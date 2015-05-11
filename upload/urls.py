# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import ChunkedUpload, GenerateUploadToken, ItemCreate

urlpatterns = patterns(
    '',
    # Upload
    url(r'^$', TemplateView.as_view(template_name="upload.html"), name='view.upload'),
    url(r'^2/$', TemplateView.as_view(template_name="upload2.html"), name='view.upload2'),
    url(r'^3/$', TemplateView.as_view(template_name="upload3.html"), name='view.upload3'),
    url(r'^api/upload/$', csrf_exempt(ChunkedUpload.as_view()), name='api.upload'),
    url(r'^api/upload/token.json$', csrf_exempt(GenerateUploadToken.as_view()), name='api.upload.token'),
    url(r'^api/item/create.json$', csrf_exempt(ItemCreate.as_view()), name='api.item.create'),
)