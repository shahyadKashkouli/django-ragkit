from .handle_message import save_message, update_saved_message, generate_rag_response, handle_rag_response
from .embeddings import qa_create_embed, search_similar_questions


def process_message(chat, asked_question_txt):
    question_record = save_message(chat, asked_question_txt)
    embed = qa_create_embed(asked_question_txt)
    similar_questions = search_similar_questions(embed)
    update_saved_message(question_record, similar_questions)
    response = handle_rag_response(question_record, similar_questions)

    return response
