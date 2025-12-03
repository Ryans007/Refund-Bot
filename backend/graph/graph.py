from langgraph.graph import StateGraph
from .state import AgentState
from .nodes import classification_node, reimbursement_node, revisor_node
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from .utils import save_graph_to_file

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(AgentState)

builder.add_node("classification", classification_node)
builder.add_node("reimbursement", reimbursement_node)
builder.add_node("revisor", revisor_node)

builder.set_entry_point("classification")

builder.add_edge("classification", "reimbursement")
builder.add_edge("reimbursement", "revisor")

graph = builder.compile(checkpointer=memory)

# save_graph_to_file(graph)
