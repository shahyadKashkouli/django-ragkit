from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http.response import JsonResponse


def ragkit_login_required() -> bool:
    return settings.RAGKIT.get("BASE_SETTING",{}).get("LOGIN_REQUIRED", False)

class RagkitLoginRequiredMixin:
    """
    Mixin for template-based views (e.g., TemplateView, DetailView).
    Redirects unauthenticated users to the login page when LOGIN_REQUIRED is enabled.
    """
    def dispatch(self, request, *args, **kwargs):
        if ragkit_login_required() and not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)


class RagkitApiLoginRequiredMixin:
    """
    Mixin for API/JSON views (e.g., ChatCreateView, ChatMessageView).
    Returns a 401 JSON response instead of redirecting unauthenticated users.
    """
    def dispatch(self, request, *args, **kwargs):
        if ragkit_login_required() and not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=401)
        return super().dispatch(request, *args, **kwargs)
