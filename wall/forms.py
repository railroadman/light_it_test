from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(max_length=10000,required=False)
    message_id = forms.IntegerField(required=False)

class CommentForm(forms.Form):
    comment_id = forms.IntegerField(required=False)
    comment_txt = forms.CharField(max_length=5000, required=False)
    message_id = forms.IntegerField(required=False)
    parent_id = forms.IntegerField(required=False)


