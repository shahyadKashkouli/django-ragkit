# Data Models

Django RAGKit provides five relational models to store your knowledge base, vector embeddings, chat sessions, user questions, and generated answers.

---

## Model Specifications

### 1. `QuestionAnswer`
Represents a curated unit of knowledge (a frequently asked question and its verified answer).

```python
class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- **`question`**: The canonical question text used to compute semantic embeddings.
- **`answer`**: The source-of-truth text provided as grounding context to the LLM.
- **Signals**: When saved or updated, Django signals automatically update corresponding `QAEmbedding` records.

---

### 2. `QAEmbedding`
Stores the dense vector representation of a `QuestionAnswer` question, equipped with an HNSW vector index.

```python
class QAEmbedding(models.Model):
    QA_foreign_key = models.ForeignKey(
        to="QuestionAnswer",
        on_delete=models.CASCADE,
        related_name="embeddings",
    )
    vector = VectorField(dimensions=dimensions)
    created_at = models.DateTimeField(auto_now_add=True)

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
```

- **`vector`**: Native PostgreSQL `vector` field configured to the dimension specified in `RAGKIT["EMBEDDING"]["DIMENSION"]`.
- **`HnswIndex`**: Hierarchical Navigable Small World index with cosine distance operators (`vector_cosine_ops`), `m=16`, and `ef_construction=64` for ultra-fast approximate nearest neighbors search.

---

### 3. `Chat`
Represents an ongoing conversational session.

```python
class Chat(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
```

- **`uuid`**: Public, non-guessable session identifier used in URL paths (`/chat/<uuid>/`).
- **`user`**: Reference to `settings.AUTH_USER_MODEL`. May be `null` when guest chats are allowed.
- **`provider` / `model`**: Snapshot of the LLM provider and model active when the chat was created.

---

### 4. `AskedQuestion`
Stores every user query submitted to a chat session.

```python
class AskedQuestion(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, related_name="questions")
    question = models.TextField()
    similar_to = models.ForeignKey(QuestionAnswer, on_delete=models.SET_NULL, null=True, blank=True)
    similarity_percentage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

- **`similar_to`**: Points to the most semantically relevant `QuestionAnswer` discovered in pgvector.
- **`similarity_percentage`**: The similarity score $(1 - \text{distance}) \times 100$.

---

### 5. `GeneratedAnswer`
Contains the response produced by the LLM for a given `AskedQuestion`.

```python
class GeneratedAnswer(models.Model):
    replied_question = models.OneToOneField(
        AskedQuestion,
        on_delete=models.CASCADE,
        related_name="generated_answer"
    )
    is_helpful = models.BooleanField(null=True, blank=True)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

- **`replied_question`**: One-to-one relationship with the user question.
- **`is_helpful`**: Optional boolean feedback score (`True`, `False`, or `None`) for tracking answer quality and fine-tuning prompt performance.
