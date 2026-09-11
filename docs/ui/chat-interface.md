# Chat Interface

Django RAGKit provides a responsive web chat interface styled with Bootstrap 5 and customized CSS.

---

## Interface Highlights

- **Dynamic Session Handling**: Initiates and preserves conversations using unique UUID tokens.
- **Asynchronous Messaging**: Sends questions and renders responses asynchronously via Fetch API without full page reloads.
- **Typing Indicator**: Real-time pulsing dots animation while the RAG retrieval and LLM generation pipeline is executing.
- **Message History**: Automatically renders previous questions and model responses when opening an existing chat session (`/chat/<uuid>/`).
- **Responsive Layout**: Fluid mobile and desktop layout built with modern flexbox and semantic HTML.

---

## Accessing the Chat UI

The default chat interface is available at:

```text
http://localhost:8000/chat/
```

When accessed directly at `/chat/`:
1. The frontend initiates a request to `/chat/create/` to instantiate a new `Chat` session.
2. The URL seamlessly updates to `/chat/<uuid>/` via the HTML5 History API.
3. Subsequent messages are posted to `/chat/<uuid>/handle-message`.


