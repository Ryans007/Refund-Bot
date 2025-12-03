from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import os
from dotenv import load_dotenv


load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

REVISOR_PROMPT = """Você é um revisor que avalia respostas geradas por outros agentes.
Avalie a confiança de acordo com a confiança da resposta, se a confiança for inferior a 70%.
sugira validação manual ou abertura de ticket interno, caso a confiança for superior a 70% devolva a resposta do Reimbursement Agent."""

revisor_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
revisor_agent = create_agent(
    revisor_model,
    system_prompt=REVISOR_PROMPT,
)