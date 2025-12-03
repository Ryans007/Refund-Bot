from langchain_core.messages import HumanMessage, SystemMessage
from ..state import AgentState
from ..agents import revisor_agent

def revisor_node(state: AgentState):
    """Revisa a resposta de reembolso com base na confiança fornecida."""
    response = revisor_agent.invoke({
        "messages": [
            HumanMessage(content="Resposta do agente de reembolso: " + state['reimbursement_answer']),
            HumanMessage(content="Confiança da resposta: " + str(state['confidence']))
        ]
    })
    print(response)
    return {
        'final_answer': response['messages'][-1].content
    }