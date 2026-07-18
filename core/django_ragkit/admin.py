from django.contrib import admin
from .models import QuestionAnswer,QAEmbedding
# Register your models here.
admin.site.register(QuestionAnswer)
admin.site.register(QAEmbedding)
