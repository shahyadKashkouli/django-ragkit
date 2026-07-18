from django.contrib.auth import get_user_model
from django.db import models
from pgvector.django import VectorField


# Create your models here.
User = get_user_model()

class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = "Question Answer"
        verbose_name_plural = "Question Answers"


class AskedQuestion(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User"
    )

    question = models.TextField(
        verbose_name="Question"
    )

    is_helpful = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Is Helpful"
    )

    similar_to = models.ForeignKey(
        to="QuestionAnswer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Similar Question"
    )

    similarity_rate = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Similarity Rate"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = "Asked Question"
        verbose_name_plural = "Asked Questions"

class QAEmbedding(models.Model):
    QA_foreign_key = models.ForeignKey(
        to="QuestionAnswer",
        on_delete=models.CASCADE,
        related_name="embeddings",
    )
    vector = VectorField(dimensions=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding #{self.pk} for QA #{self.QA_foreign_key_id}"