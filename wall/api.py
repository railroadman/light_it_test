from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import logging
from django.core import serializers
from django.views.generic import TemplateView, View
from django.db.models import Count
from models import Messages, Comments
from soc_auth.models import Authors
from utils import build_from_db
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from .forms import CommentForm,MessageForm



def index_page(request):
        template_name = "wall/index.html"
        logger = logging.getLogger(__name__)
        logger.info("SHOW ALL MESSAGES")
        page = 1
        if request.user.is_authenticated():
            user_info = Authors.objects.get(user=request.user)
        messages = Messages.objects.annotate(comments_count=Count('comment')).filter(status=1).order_by('-created_at')
        if messages:
            paginator = Paginator(messages, 10)
            try:
                messages = paginator.page(page)
            except PageNotAnInteger:

                messages = paginator.page(1)
            except Exception as e:
                messages = None

            logger.info(messages[0].comments_count)
        return render(request, template_name, {'messages': messages})

class ApiWallView(View):
    template_name = "wall/index.html"
    logger = logging.getLogger(__name__)

    def get(self, request):
        self.logger.info("API:GET ALL MESSAGES or PARTIAL")
        page = request.GET.get('page')
        if request.user.is_authenticated():
            user_info = Authors.objects.get(user=request.user)

        messages = Messages.objects.annotate(comments_count=Count('comment')).filter(status=1).order_by(
            '-created_at').all()
        paginator = Paginator(messages, 10)
        try:
            messages = paginator.page(page)
        except Exception as e:
            self.logger.info(e)
            messages = None
        # self.logger.info(messages[0].comments_count)
        if not messages:
            return HttpResponse("0")
        else:
            data = [
                {'msg_id': m.id, 'message': m.message, 'created_at': m.created_at.strftime("%Y-%m-%d %H:%M"),
                 'author_id': m.author.user.id, 'author_name': m.author.user.username,
                 'author_photo': m.author.photo, 'count': m.comments_count, 'time_ago': m.time_ago} for m in messages]
            if request.user.is_authenticated():
                for d in data:
                    if d['author_id'] == request.user.id:
                        d['is_owner'] = 1
            return JsonResponse(data, safe=False)

    def post(self, request):
        f = MessageForm({'message':request.POST.get('msg_text')})
        if f.is_valid() and request.POST.get('msg_text')!='':
            msg_text = f.cleaned_data['message']
            author = request.user.authors
            m = Messages.objects.create(message=msg_text, author=author)
            m.save()
            return HttpResponse(m.pk)
        else:
            return JsonResponse(f.errors,safe=False)
        # request.forms['parent_id']

    def put(self, request):
        put = QueryDict(request.body)
        f = MessageForm({'message': put.get('msg_text'),'message_id':put.get('msg_id')})
        if f.is_valid():
            msg_id = f.cleaned_data['message_id']
            msg_text = f.cleaned_data['message']
            m = Messages.objects.filter(pk=msg_id, author=request.user.authors)[0]
            if not m:
                self.logger.info("PUT/UPDATE ERROR:NOT FOUND message for %s" % (m.id))
                return HttpResponse("false")
            else:
                self.logger.info("PUT/UPDATE message for: %s with text: %s", msg_id, msg_text)
                m.message = msg_text
                m.save()
                return JsonResponse({"msg_id": m.pk, "msg_text": msg_text}, safe=False)
        else:
            return JsonResponse(f.errors,safe=False)

    def delete(self, request):
        delete = QueryDict(request.body)

        f = MessageForm({'message_id':delete.get('msg_id')})
        if f.is_valid():
            msg_id = f.cleaned_data['message_id']
            m = Messages.objects.get(pk=msg_id)
            m.status = 0
            m.save()
            return HttpResponse("deleted")
        else:
            return JsonResponse(f.errors,safe=False)


class ApiCommentView(TemplateView):
    template_name = "wall/comments.html"
    logger = logging.getLogger(__name__)

    def put(self, request):
        put = QueryDict(request.body)
        f = CommentForm({"comment_id":put.get('ed_comment_id'),"comment_txt":put.get('ed_comment_txt').strip()})
        if f.is_valid():
            cmnt_id = f.cleaned_data['comment_id']
            cmnt_text = f.cleaned_data['comment_txt']
            c = Comments.objects.filter(pk=cmnt_id, author=request.user.authors)[0]
            if not c:
                self.logger.info("PUT/UPDATE ERROR:NOT FOUND comment for %s" % (c.id))
                return HttpResponse("false")
            else:
                if c.status == 1:
                    self.logger.info("PUT/UPDATE comment for: %s with text: %s", cmnt_id, cmnt_text)
                    c.comment_txt = cmnt_text
                    c.save()
                else:
                    cmnt_text = c.comment_txt
                return JsonResponse({"cmnt_id": c.pk, "cmnt_text": cmnt_text}, safe=False)
        else:
            return JsonResponse(f.errors,safe=False)

    def delete(self, request):
        delete = QueryDict(request.body)
        f = CommentForm({"comment_id": delete.get('cmnt_id')})
        if f.is_valid():
            cmnt_id = f.cleaned_data['comment_id']
            if cmnt_id:
                self.logger.info("DELETING COMMENT ID:%s", cmnt_id)
                c = Comments.objects.get(pk=cmnt_id)
                if (c.author == request.user.authors):
                    c.comment_txt = "Message was deleted"
                    c.status = 0
                    c.save()
                    return JsonResponse({"cmnt_id": c.pk})
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return JsonResponse(f.errors,safe=False)

    def get(self, request, *args, **kwargs):
        tree = {}
        f = CommentForm({"message_id":request.GET.get('msg_id')})
        if f.is_valid():

            msg_id = f.cleaned_data['message_id']
            if msg_id:
                self.logger.info("SHOW COMMMENTS FOR MESSAGE %s", [msg_id])
                c = Comments.objects.filter(message__pk=msg_id)
                lookup = build_from_db(c, msg_id, user_id=request.user.id)
                if lookup != {}:
                    roots = lookup[0]['childrens']
                    for r in roots:
                        if 'childrens' in r:
                            if r['childrens'] == []:
                                r['childrens'] = None
                    tree['childrens'] = roots
                    tree['user_id'] = request.user.id
                    tree['msg_id'] = msg_id;
                    return JsonResponse(tree, safe=False)
                else:
                    empty = {"msg_id": msg_id, "childrens": None, "user_id": request.user.id}
                    return JsonResponse(empty, safe=False)
            else:
                return HttpResponse("please provide message id for getting comments")
        else:
            return JsonResponse(f.errors,safe=False)

    def post(self, request, *args, **kwarg):
        self.logger.info(" I AM IN COMMENT POST")
        f =  CommentForm({"message_id":request.POST.get('msg_id'),"parent_id":request.POST.get('parent_id'),"comment_txt":request.POST.get('msg_text')})
        if f.is_valid():
            m = Messages.objects.get(pk=f.cleaned_data['message_id'])
            c = Comments.objects.create(comment_txt=f.cleaned_data['comment_txt'], message=m, parent_id=f.cleaned_data['parent_id'], author=request.user.authors)
            c.save()
            return HttpResponse(c.pk)
        else:
            return JsonResponse(f.errors,safe=False)


