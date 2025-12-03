from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from ..tools.vector_store_tool import search_in_vectorstore_tool
import os

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

class ClassificationResult(BaseModel):
    label: str
    explaination: str

# Prompt do agente de classificação
CLASSIFICATION_PROMPT = """Você é um classificador de mensagens. Classifique a mensagem do usuário em uma das categorias fornecidas.
Categorias possíveis: Reembolso, Cancelamento, Financeiro, Exceções, Suporte, Entrega, Pedido, Fraude de acordo com a base de conhecimento:
use a ferramenta search_in_vectorstore_tool para consultar a base de conhecimento
Explaination: Explique o porque tomou essa decisão"""

classification_model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
classification_agent = create_agent(
    classification_model,
    system_prompt=CLASSIFICATION_PROMPT,
    tools=[search_in_vectorstore_tool],
    response_format=ToolStrategy(ClassificationResult),
)
