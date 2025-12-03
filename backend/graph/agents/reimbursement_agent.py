from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from ..tools.vector_store_tool import search_in_vectorstore_tool
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

class ReimbursementAgentOutput(BaseModel):
    answer: str
    confidence: float

REIMBURSEMENT_PROMPT = """Você é um agente interno que auxilia colaboradores a decidirem sobre reembolsos e cancelamentos.
Você ja tem a classificação da mensagem e a explicação para essa classificação que virá de outro agente.
Consulte a base de conhecimento:
utilize a ferramente search_in_vectorstore_tool para buscar informações relevantes na base de conhecimento sobre reembolsos e políticas.
Sempre consulte a base de conhecimento antes de responder.
Sempre cite a politica ao qual sua resposta se baseia.
E classifique a confiança da sua resposta com base na relação dela coma base de conhecimento."""

reimbursement_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
reimbursement_agent = create_agent(
    reimbursement_model,
    system_prompt=REIMBURSEMENT_PROMPT,
    tools=[search_in_vectorstore_tool],
    response_format=ToolStrategy(ReimbursementAgentOutput),
)