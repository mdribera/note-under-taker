from django.contrib import admin
from .models import Note, Label

admin.site.register(Note)
admin.site.register(Label)