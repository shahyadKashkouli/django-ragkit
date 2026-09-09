from django_ragkit.models import AskedQuestion, GeneratedAnswer
from django_ragkit.providers.LLM.factory import get_LLM_provider
from django_ragkit.services.prompts import build_rag_prompt
from django.conf import settings
from .prompts import defualt_not_found_prompt


def save_message(chat, question):
    return AskedQuestion.objects.create(question=question, chat=chat)


def update_saved_message(question_record, similar_questions):
    most_similar = similar_questions.first()
    question_record.similar_to_id = most_similar.QA_foreign_key_id
    question_record.similarity_percentage = (1 - most_similar.distance) * 100

    question_record.save(
        update_fields=[
            "similar_to",
            "similarity_percentage",
        ]
    )


def save_generated_answer(question_record, llm_answer):
    return GeneratedAnswer.objects.create(replied_question=question_record, answer=llm_answer)


def get_not_found_response():
    not_found_prompt = settings.RAGKIT.get("LLM").get("OPTIONS", {}).get("NOT_FOUND_PROMPT", defualt_not_found_prompt)
    return not_found_prompt


def generate_rag_response(question, similar_questions):
    if not similar_questions:
        return get_not_found_response()

    best_similarity_percentage = (1 - similar_questions[0].distance) * 100

    if best_similarity_percentage < 50:
        return get_not_found_response()

    llm = get_LLM_provider()
    response = llm.generate_response(build_rag_prompt(question, similar_questions))
    return response


def handle_rag_response(question_record, similar_questions):
    question = question_record.question
    response = generate_rag_response(question, similar_questions)
    save_generated_answer(question_record, response)
    return response