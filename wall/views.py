from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import logging
import json
from django.views.generic import TemplateView
from django.db.models import Count
from models import Messages, Comments
from soc_auth.models import Authors
from utils import build_from_db
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


class WallView(TemplateView):
    template_name = "wall/index.html"
    logger = logging.getLogger(__name__)

    def get(self, request):
        self.logger.info("SHOW ALL MESSAGES")
        page = 1
        if request.user.is_authenticated():
            user_info = Authors.objects.get(user=request.user)
            self.logger.info(request.user)
            self.logger.info(request.user.authors.photo)

        messages = Messages.objects.annotate(comments_count=Count('comment')).filter(status=1).order_by('-created_at')
        paginator = Paginator(messages, 10)
        messages = paginator.page(page)
        self.logger.info(messages[0].comments_count)

        return render(request, self.template_name, {'messages': messages})

    def post(self, request):
        msg_text = request.POST.get('msg_text')
        parent_id = request.POST.get('parent_id')
        author = request.user.authors
        m = Messages.objects.create(message=msg_text, author=author)
        m.save()
        return HttpResponse("saved")
        # request.forms['parent_id']


class CommentView(TemplateView):
    template_name = "wall/comments.html"
    logger = logging.getLogger(__name__)

    def get(self, request, *args, **kwargs):
        self.logger.info("SHOW COMMMENTS FOR MESSAGE %s", [kwargs['msg_id']])
        self.logger.info(kwargs)
        message = Messages.objects.filter(status=1, pk=kwargs['msg_id'])[0]
        return render(request, self.template_name, {"message": message, 'message_id': kwargs['msg_id'],
                                                    "action_url": "/wall/" + kwargs['msg_id'] + "/"})

    def post(self, request, *args, **kwarg):
        self.logger.info(" I AM IN POST")
        msg_text = request.POST.get('msg_text')
        self.logger.info(request.POST.get('msg_id'))
        m = Messages.objects.get(pk=request.POST.get('msg_id'))
        parent_id = request.POST.get('parent_id')
        Comments.objects.create(comment_txt=msg_text, message=m, parent_id=parent_id, author=request.user.authors)
        return redirect("/wall/%s" % (str(m.id)))

    def arrange_comments_for(self, msg_id):
        comments = Messages.objects.filter(status=1, parent_id=msg_id)


def delete_msg(request, msg_id):
    logger = logging.getLogger(__name__)
    logger.info("DELETING OBJECT %s", [msg_id])
    m = Messages.objects.get(pk=msg_id)
    m.status = 0
    m.save()
    return HttpResponse("deleted")


def delete_comment(request, comment_id):
    logger = logging.getLogger(__name__)
    logger.info("DELETING COMMENT %s", [comment_id])
    c = Comments.objects.get(pk=comment_id)
    c.status = 0
    c.save()
    return HttpResponse("ok")


def get_tree(request, msg_id):
    s = {}
    c = Comments.objects.filter(message__pk=msg_id)
    # print(c)
    lookup = build_from_db(c, msg_id)  # can look at any node from here.
    # print(lookup)
    # roots = [x for x in lookup.values() if x.parent is None]
    # print(roots[0]['childrens'])
    roots = lookup[0]['childrens']
    for r in roots:
        if 'childrens' in r:
            if r['childrens'] == []:
                r['childrens'] = None
    s['childrens'] = roots
    return JsonResponse(s, safe=False)


def draw_tree(request, msg_id):

    return render(request, "wall/draw_tree.html",{"msg_id":msg_id})
