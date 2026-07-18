from django_ragkit.providers.embeddings.factory import get_embedding_provider
from django_ragkit.models import QAEmbedding
def qa_create_embed(question):
    provider = get_embedding_provider()
    vector = provider.embed(question)
    return vector
def qa_save_embed(qa_foreign_key,vector):
    QAEmbedding.objects.create(
        QA_foreign_key=qa_foreign_key,
        vector=vector,
    )

def qa_create_and_save_embed(qa):
    vector = qa_create_embed(qa.question)
    qa_save_embed(qa, vector)

