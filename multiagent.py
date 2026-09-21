from langgraph.graph import StateGraph, START, END

from state.state import AgentState

from agents.supervisor import supervisor
from agents.researcher import researcher
from agents.developer import developer
from agents.reviewer import reviewer
from agents.final_agent import final_agent


# --------------------------------------------------
# Routing function
# --------------------------------------------------

def route_from_supervisor(state: AgentState):

    next_agent = state["next_agent"]

    if next_agent == "researcher":
        return "researcher"

    if next_agent == "developer":
        return "developer"

    if next_agent == "reviewer":
        return "reviewer"

    if next_agent == "FINISH":
        return "final_agent"

    return "final_agent"


# --------------------------------------------------
# Create graph
# --------------------------------------------------

builder = StateGraph(AgentState)


# --------------------------------------------------
# Add nodes
# --------------------------------------------------

builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "researcher",
    researcher
)

builder.add_node(
    "developer",
    developer
)

builder.add_node(
    "reviewer",
    reviewer
)

builder.add_node(
    "final_agent",
    final_agent
)


# --------------------------------------------------
# START → SUPERVISOR
# --------------------------------------------------

builder.add_edge(
    START,
    "supervisor"
)


# --------------------------------------------------
# Supervisor → Dynamic Agent
# --------------------------------------------------

builder.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {
        "researcher": "researcher",
        "developer": "developer",
        "reviewer": "reviewer",
        "final_agent": "final_agent"
    }
)


# --------------------------------------------------
# Every worker returns to supervisor
# --------------------------------------------------

builder.add_edge(
    "researcher",
    "supervisor"
)

builder.add_edge(
    "developer",
    "supervisor"
)

builder.add_edge(
    "reviewer",
    "supervisor"
)


# --------------------------------------------------
# Final agent → END
# --------------------------------------------------

builder.add_edge(
    "final_agent",
    END
)


# --------------------------------------------------
# Compile
# --------------------------------------------------

graph = builder.compile()