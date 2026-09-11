# Signals & Auto-Indexing

Django RAGKit includes built-in Django signals that eliminate manual vectorization workflows. Whenever knowledge entries are created or updated, their vector representations are automatically computed and indexed.

---

## Implementation Details

The signal receivers are registered in `django_ragkit/signals.py` and connected when the Django app initializes.

### 1. Automatic Creation (`post_save`)

When a new `QuestionAnswer` instance is saved for the first time:

```python
@receiver(post_save, sender=QuestionAnswer)
def create_embedding(sender, instance, created, **kwargs):
    if created:
        qa_create_and_save_embed(instance)
```

1. Checks if `created` is `True`.
2. Sends `instance.question` to the configured embedding provider.
3. Inserts a new row in `QAEmbedding` linked to this `QuestionAnswer`.
4. The PostgreSQL HNSW index automatically incorporates the new vector.

### 2. Automatic Updates (`pre_save`)

When an existing `QuestionAnswer` instance is modified:

```python
@receiver(pre_save, sender=QuestionAnswer)
def update_embedding(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = QuestionAnswer.objects.get(pk=instance.pk)
    if old.question != instance.question:
        vector = qa_create_embed(instance.question)
        QAEmbedding.objects.filter(QA_foreign_key=instance).update(vector=vector)
```

1. Inspects the previous database state using `instance.pk`.
2. Compares `old.question` against the incoming `instance.question`.
3. If the question string was changed:
   - Recalculates the vector embedding.
   - Updates the associated `QAEmbedding` row in-place.
4. If only the `answer` was modified, the embedding calculation is skipped, saving network bandwidth and API costs.

---

## App Initialization

To ensure signals are properly registered, `django_ragkit/apps.py` imports them in the `ready()` lifecycle method:

```python title="apps.py"
from django.apps import AppConfig

class DjangoRagkitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_ragkit'

    def ready(self):
        import django_ragkit.signals
```
