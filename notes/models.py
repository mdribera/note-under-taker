from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.db import models

class Note(models.Model):
  note_title = models.CharField(max_length=200)
  note_text = models.TextField(max_length=1000)
  pub_date = models.DateTimeField('date published')
  labels = models.ManyToManyField('Label', related_name='notes')

  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

  def __str__(self):
    return self.note_title

class Label(models.Model):
  text = models.CharField(max_length=200, default="")
  background_color = models.CharField(max_length=6, default="ffffff")
  text_color = models.CharField(max_length=6, default="000000")

  def __str__(self):
    return self.text
