from django.contrib.auth import get_user_model
from django.db import models
from pgvector.django import VectorField, HnswIndex
import uuid

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
    class Meta:
        indexes = [
            HnswIndex(
                name="qa_embedding_hnsw_idx",
                fields=["vector"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


class Chat(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="chat uuid"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User"
    )

    provider = models.CharField(
        max_length=50,
        verbose_name="Provider"
    )

    model = models.CharField(
        max_length=100,
        verbose_name="Model"
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ["-id"]


class AskedQuestion(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.SET_NULL, null=True, related_name="questions",
                             verbose_name="Chat")

    question = models.TextField(
        verbose_name="Question"
    )
    similar_to = models.ForeignKey(
        to="QuestionAnswer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Most Similar Question"
    )
    similarity_percentage = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Max Similarity Percentage"
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


class GeneratedAnswer(models.Model):
    replied_question = models.OneToOneField(
        to=AskedQuestion,
        on_delete=models.CASCADE,
        related_name="generated_answer",
        verbose_name="Replied Question"
    )

    is_helpful = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Is Helpful"
    )

    answer = models.TextField(
        verbose_name="Answer"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Generated Answer"
        verbose_name_plural = "Generated Answers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Answer #{self.pk} ({self.replied_question.question} )"
