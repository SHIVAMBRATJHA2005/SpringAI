from typing import TypedDict, Annotated

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage


# 1. Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def search_product(product: str) -> str:
    """Search for information about a product."""
    return f"Information found for {product}"


tools = [multiply, search_product]


# 2. Create LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


# 3. Define graph state
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 4. LLM node
def chatbot(state: State):

    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


# 5. Tool node
tool_node = ToolNode(tools)


# 6. Decide whether to call a tool
def should_continue(state: State):

    last_message = state["messages"][-1]

    # LLM requested a tool
    if last_message.tool_calls:
        return "tools"

    # LLM produced final answer
    return END


# 7. Build graph
graph = StateGraph(State)

graph.add_node("agent", chatbot)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

# After tool execution, send result back to LLM
graph.add_edge("tools", "agent")


app = graph.compile()


# 8. Run
result = app.invoke({
    "messages": [
        ("user", "What is 25 multiplied by 4?")
    ]
})

print(result["messages"][-1].content)