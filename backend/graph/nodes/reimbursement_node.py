from ..agents import reimbursement_agent
from ..state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage

def reimbursement_node(state: AgentState):
    """Fornece uma resposta de reembolso com base na mensagem do usuário, classificação e explicação."""
    response = reimbursement_agent.invoke({
        "messages": [
            HumanMessage(content="Classificação da mensagem: " + state['label']),
            HumanMessage(content="Explicação da classificação: " + state['classification_agent_explaination']),
            HumanMessage(content="Mensagem do usuário: " + state['user_message'])
        ]
    })
    return {
        'reimbursement_answer': response['structured_response'].answer,
        'confidence': response['structured_response'].confidence
    }