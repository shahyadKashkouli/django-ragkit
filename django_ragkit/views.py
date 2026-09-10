from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, TemplateView
from .models import Chat
from .providers.LLM.factory import get_LLM_provider
from .services.chat import process_message
from .forms import AskedQuestionModelForm
from django.http.response import JsonResponse
from .services.auth_helper import ragkit_login_required , RagkitLoginRequiredMixin , RagkitApiLoginRequiredMixin

# Create your views here.






class ChatView(RagkitLoginRequiredMixin, TemplateView):
    template_name = 'django_ragkit/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = AskedQuestionModelForm()
        return data


class ChatCreateView(RagkitApiLoginRequiredMixin, View):
    """
    Creates a new chat session using the configured LLM provider and model.
    Associates the chat with the authenticated user when available, while
    allowing guest users when authentication is not required.
    """
    def post(self, request):
        llm_model = get_LLM_provider()

        user = request.user if request.user.is_authenticated else None

        chat = Chat.objects.create(
            user=user,
            provider=llm_model.provider,
            model=llm_model.model,
        )

        return JsonResponse({
            "uuid": str(chat.uuid)
        })


class ChatDetailView(RagkitLoginRequiredMixin, DetailView):
    """
    Displays a chat and restricts access based on the authentication setting.
    Authenticated users can access their own chats and guest chats when
    authentication is optional, while unauthenticated users can only access
    guest chats.
    """
    template_name = 'django_ragkit/chat.html'
    model = Chat
    context_object_name = "chat"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        queryset = super().get_queryset()

        if ragkit_login_required():
            return queryset.filter(user=self.request.user)

        if self.request.user.is_authenticated:
            return queryset.filter(Q(user=self.request.user) | Q(user__isnull=True))

        return queryset.filter(user__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AskedQuestionModelForm()
        return context


class ChatMessageView(RagkitApiLoginRequiredMixin, View):
    """
    Processes a message for a chat after verifying that the user has access
    to the chat. Validates the submitted question, generates an answer, and
    returns it as a JSON response.
    """
    def post(self, request, uuid):
        qs = Chat.objects.all()

        if ragkit_login_required():
            qs = qs.filter(user=request.user)
        elif request.user.is_authenticated:
            qs = qs.filter(Q(user=request.user) | Q(user__isnull=True))
        else:
            qs = qs.filter(user__isnull=True)

        chat = get_object_or_404(qs, uuid=uuid)

        form = AskedQuestionModelForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)

        question = form.cleaned_data.get("question")
        answer = process_message(chat, question)
        return JsonResponse({"answer": answer}, status=200)