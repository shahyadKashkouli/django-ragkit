# Authentication & Permissions

Django RAGKit provides granular access control that seamlessly integrates with Django's standard authentication system (`django.contrib.auth`).

---

## Configuration

Control whether user login is strictly enforced using the `LOGIN_REQUIRED` key in `settings.py`:

```python title="settings.py"
RAGKIT = {
    "BASE_SETTING": {
        "LOGIN_REQUIRED": True,  # Default is False
    },
    # ...
}
```

---

## Access Modes Comparison

| Mode | `LOGIN_REQUIRED = False` (Default) | `LOGIN_REQUIRED = True` (Strict) |
| :--- | :--- | :--- |
| **Anonymous / Guest Access** | Allowed. Sessions are created with `user = None`. | Blocked. Anonymous visitors are redirected to login. |
| **Template Views** (`/chat/`, `/chat/<uuid>/`) | Accessible to all visitors. | Redirects unauthenticated visitors to `settings.LOGIN_URL`. |
| **API Endpoints** (`/chat/create/`, `/handle-message`) | Processes guest sessions and authenticated sessions. | Returns HTTP 401 with `{"error": "Authentication required."}`. |
| **Session Isolation** | Authenticated users see their own chats. Anonymous visitors can view unassigned guest chats. | Users can only view and message chats strictly assigned to their `user_id`. |

---

## Built-in Mixins

Django RAGKit defines specialized mixins in `django_ragkit.services.auth_helper`:

### 1. `RagkitLoginRequiredMixin`
Used on template-rendering views (such as `ChatView` and `ChatDetailView`):

```python
class RagkitLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if ragkit_login_required() and not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)
```

### 2. `RagkitApiLoginRequiredMixin`
Used on JSON API views (such as `ChatCreateView` and `ChatMessageView`):

```python
class RagkitApiLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if ragkit_login_required() and not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=401)
        return super().dispatch(request, *args, **kwargs)
```

---

## User Association & Session Privacy

When an authenticated user creates a chat session:
```python
chat = Chat.objects.create(
    user=request.user if request.user.is_authenticated else None,
    provider=llm_model.provider,
    model=llm_model.model,
)
```

In `ChatDetailView` and `ChatMessageView`, querysets are strictly filtered to ensure that users cannot access, read, or send messages into another user's chat session:

```python
if ragkit_login_required():
    qs = qs.filter(user=request.user)
elif request.user.is_authenticated:
    qs = qs.filter(Q(user=request.user) | Q(user__isnull=True))
else:
    qs = qs.filter(user__isnull=True)
```
