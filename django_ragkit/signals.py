from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_ragkit.models import QuestionAnswer, QAEmbedding
from django_ragkit.services.embeddings import qa_create_and_save_embed, qa_create_embed


@receiver(post_save, sender=QuestionAnswer)
def create_embedding(sender, instance, created, **kwargs):
    if created:
        qa_create_and_save_embed(instance)


@receiver(pre_save, sender=QuestionAnswer)
def update_embedding(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = QuestionAnswer.objects.get(pk=instance.pk)
    if old.question != instance.question:
        vector = qa_create_embed(instance.question)
        QAEmbedding.objects.filter(QA_foreign_key=instance).update(vector=vector)
