from langchain_core.tools import tool
from ..insertion import vectorstore

@tool
def search_in_vectorstore_tool(query: str) -> str:
    """Busca informações na base de conhecimento sobre reembolsos e políticas."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "fetch_k": 21})
    docs = retriever.invoke(query)

    results = "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    return results if results else "Nenhuma informação relevante encontrada."