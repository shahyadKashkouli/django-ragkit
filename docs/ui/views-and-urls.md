# Views & URLs

Django RAGKit provides four class-based views for rendering conversations, creating sessions, and processing questions.

---

## URL Endpoints

To include Django RAGKit's endpoints in your project:

```python title="urls.py"
from django.urls import path, include

urlpatterns = [
    path("", include("django_ragkit.urls")),
]
```

This exposes the following URL routes:

| URL Pattern | View Name | Class-Based View | HTTP Methods | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/chat/` | `chat-page` | `ChatView` | `GET` | Renders a fresh chat session page |
| `/chat/create/` | `chat-create` | `ChatCreateView` | `POST` | Instantiates a new chat session and returns its UUID |
| `/chat/<uuid:uuid>/` | `chat-detail-page` | `ChatDetailView` | `GET` | Displays existing conversation history for a given UUID |
| `/chat/<uuid:uuid>/handle-message` | `handle-message` | `ChatMessageView` | `POST` | Processes a user question through the RAG pipeline and returns the answer |

---

## Detailed View Reference

### 1. `ChatView`
Renders the primary chat landing template (`django_ragkit/chat.html`).
- **Inheritance**: `RagkitLoginRequiredMixin`, `TemplateView`
- **Context Data**: Includes an instance of `AskedQuestionModelForm`.

### 2. `ChatCreateView`
An API view that instantiates a new `Chat` record.
- **Inheritance**: `RagkitApiLoginRequiredMixin`, `View`
- **Behavior**:
  - Fetches the active LLM provider from the factory.
  - Sets `chat.user` to `request.user` if authenticated, or `None` if guest.
  - Returns a JSON payload:
    ```json
    {
      "uuid": "4c43ad1a-0518-472d-9860-9fa6b36bf4fe"
    }
    ```

### 3. `ChatDetailView`
Renders historical messages for an existing session.
- **Inheritance**: `RagkitLoginRequiredMixin`, `DetailView`
- **Lookup Field**: `uuid`
- **Permissions**:
  - When `LOGIN_REQUIRED = True`: Restricts access strictly to chats where `chat.user == request.user`.
  - When `LOGIN_REQUIRED = False`: Authenticated users can view their own chats and guest chats; unauthenticated users can view guest chats.

### 4. `ChatMessageView`
Executes the RAG pipeline for an incoming user query.
- **Inheritance**: `RagkitApiLoginRequiredMixin`, `View`
- **Input Parameters**:
  - `uuid`: URL path parameter identifying the chat session.
  - `question`: POST form body containing the question string.
- **Response**:
  - `200 OK`: `{"answer": "Your synthesized response..."}`
  - `400 Bad Request`: `{"error": { ...validation errors... }}`
  - `401 Unauthorized`: `{"error": "Authentication required."}` (if login enforced)
  - `404 Not Found`: If session UUID does not exist or user lacks permission.
