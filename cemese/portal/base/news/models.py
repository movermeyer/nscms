#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from photologue.models import ImageModel
from taggit.managers import TaggableManager

from cemese.db.models import ContentModel


class BaseNews(ContentModel):
    body = RichTextField()
    tags = TaggableManager(blank=True)

    class Admin(ContentModel.Admin):
        date_hierarchy = "publish_date"
        search_fields = ("title", "description", "body", )
        list_filter = ("published", )
        list_display = ("title", "admin_thumbnail", "published", "publish_date", )
        fieldsets = (
            (None, {"fields": ("title", "tags", "description", "image", "body", )}),
            (_(u"Publicação"), {"fields": ("published", "publish_date", "expire_date", )}),
        )
        
    class Meta:
        ordering = ['-publish_date']
        verbose_name = _(u"Notícia")
        verbose_name_plural = _(u"Notícias")
        abstract = True

    def related_by_tags(self, count=10):
        qs = self.__class__.objects.published(order_by=None)
        qs = qs.filter(tags__pk__in=[i.pk for i in self.tags.all()]).exclude(pk=self.id)
        return qs[:count]
