from ..agents import classification_agent
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import AgentState
from ..tools.vector_store_tool import search_in_vectorstore_tool

def classification_node(state: AgentState):
    """Classifica a mensagem do usuário em uma das categorias fornecidas."""
    response = classification_agent.invoke({
        "messages":[
            {"role": "user", "content": state['user_message']}
        ]
    })
    return {
        'label': response['structured_response'].label,
        'classification_agent_explaination': response['structured_response'].explaination
    }