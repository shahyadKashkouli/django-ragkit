from django.contrib import admin
from .models import QuestionAnswer,QAEmbedding,Chat,AskedQuestion,GeneratedAnswer
# Register your models here.
admin.site.register(QuestionAnswer)
admin.site.register(QAEmbedding)
admin.site.register(Chat)
admin.site.register(AskedQuestion)
admin.site.register(GeneratedAnswer)
