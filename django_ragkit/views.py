from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, TemplateView
from .models import Chat
from .providers.LLM.factory import get_LLM_provider
from .services.chat import process_message
from .forms import AskedQuestionModelForm
from django.http.response import JsonResponse


# Create your views here.


class ChatView(TemplateView):
    template_name = 'django_ragkit/chat.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = AskedQuestionModelForm()
        return data


class ChatCreateView(View):
    def post(self, request):
        llm_model = get_LLM_provider()

        chat = Chat.objects.create(
            user=request.user,
            provider=llm_model.provider,
            model=llm_model.model,
        )

        return JsonResponse({
            "uuid": str(chat.uuid)
        })

class ChatDetailView(DetailView):
    template_name = 'django_ragkit/chat.html'
    model = Chat
    context_object_name = "chat"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AskedQuestionModelForm()
        return context


class ChatMessageView(View):
    def post(self, request, uuid):
        chat = get_object_or_404(Chat, uuid=uuid, user=request.user)
        form = AskedQuestionModelForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)
        question = form.cleaned_data.get("question")
        answer = process_message(chat, question)
        return JsonResponse({"answer": answer}, status=200)
