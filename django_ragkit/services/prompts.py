from django.conf import settings

default_base_prompt = """
You are a friendly and helpful assistant.
Answer the user's questions based on the provided context.
Use a natural, conversational tone, as if you're talking to a friend.
Keep your answers clear, concise, and easy to understand.
If the answer is not available in the provided context, say so honestly.
Respond using the same language as `user_question`.
"""
defualt_not_found_prompt = """
Sorry, I couldn't find information about that. Please contact support for assistance.
"""


def build_rag_prompt(question, similar_questions):
    base_prompt = settings.RAGKIT.get("LLM").get("OPTIONS", {}).get("BASE_PROMPT", default_base_prompt)
    not_found_prompt = settings.RAGKIT.get("LLM").get("OPTIONS", {}).get("NOT_FOUND_PROMPT", defualt_not_found_prompt)
    similar_questions_dict = {q.QA_foreign_key.question: q.QA_foreign_key.answer for q in similar_questions}
    final_prompt = {
        "system_prompt": base_prompt,
        "fallback_prompt": not_found_prompt,
        "user_question": question,
        "dataset": similar_questions_dict
    }
    return final_prompt
