# RAG Pipeline

This document explains the end-to-end lifecycle of a query in Django RAGKit, from user message reception to vector search, prompt assembly, and response generation.

---

## Step-by-Step Breakdown

### 1. Request Handling & Authorization
When a user sends a message, `ChatMessageView` intercepts the POST request at `/chat/<uuid>/handle-message`.
- Access is verified through `RagkitApiLoginRequiredMixin` according to the `LOGIN_REQUIRED` setting.
- The `Chat` session is fetched and ownership is verified.
- The input payload is validated via `AskedQuestionModelForm`.

### 2. Message Persistence
Before invoking any external AI services, the incoming query is stored in the database:
```python
question_record = save_message(chat, asked_question_txt)
```
This guarantees an immutable audit log of all questions asked, even if downstream network requests fail.

### 3. Vector Embedding Generation
The question string is passed to the configured embedding provider (`OllamaEmbeddingProvider` or `OpenRouterEmbeddingProvider`):
```python
embed = qa_create_embed(asked_question_txt)
```
The provider returns a normalized dense vector (e.g. 1024 or 768 dimensions).

### 4. pgvector Cosine Search
Using pgvector's `CosineDistance` expression, Django queries the `QAEmbedding` table:
```python
def search_similar_questions(embedding, limit=5):
    return (
        QAEmbedding.objects
        .annotate(distance=CosineDistance("vector", embedding))
        .select_related("QA_foreign_key")
        .order_by("distance")[:limit]
    )
```
Because the `QAEmbedding` table utilizes an **HNSW (Hierarchical Navigable Small World)** index (`vector_cosine_ops`), this similarity search operates in sub-millisecond time even across hundreds of thousands of documents.

### 5. Similarity Scoring & Threshold Verification
Cosine distance in pgvector ranges from `0.0` (identical) to `2.0` (opposite).

Django RAGKit calculates the similarity percentage as:

```text
Similarity % = (1 - distance) * 100
```

The query record is annotated with the closest matching question and its score:
```python
best_similarity_percentage = (1 - similar_questions[0].distance) * 100
```

> [!IMPORTANT]
> **50% Relevance Threshold**:
> If the closest match has a similarity percentage below **50%**, Django RAGKit halts further LLM inference and immediately returns the configured `NOT_FOUND_PROMPT`. This prevents model hallucination and unnecessary API costs.

### 6. Prompt Construction
If similarity exceeds 50%, a structured prompt payload is constructed:
```python
final_prompt = {
    "system_prompt": base_prompt,
    "fallback_prompt": not_found_prompt,
    "user_question": question,
    "dataset": {
        q.QA_foreign_key.question: q.QA_foreign_key.answer
        for q in similar_questions
    }
}
```

### 7. LLM Generation & Response Storage
The assembled payload is sent to the LLM provider. The output is captured, persisted as a `GeneratedAnswer` linked to the `AskedQuestion`, and returned to the frontend as JSON.
