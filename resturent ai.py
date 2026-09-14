from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq


# -----------------------------
# 1. LLM
# -----------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# -----------------------------
# 2. State
# -----------------------------

class RestaurantState(TypedDict):
    messages: list
    intent: str
    response: str


# -----------------------------
# 3. Restaurant tools
# -----------------------------

def search_restaurants(location: str, cuisine: str):
    """
    Dummy restaurant database.
    """

    restaurants = [
        {
            "name": "La Piazza",
            "cuisine": "Italian",
            "location": "Asansol",
            "rating": 4.5
        },
        {
            "name": "Roma Kitchen",
            "cuisine": "Italian",
            "location": "Asansol",
            "rating": 4.2
        }
    ]

    return restaurants


def check_availability(restaurant: str, people: int, time: str):

    # Normally this would query a real database.

    return {
        "restaurant": restaurant,
        "people": people,
        "time": time,
        "available": True
    }


# -----------------------------
# 4. Agent node
# -----------------------------

def agent_node(state: RestaurantState):

    messages = state["messages"]

    prompt = f"""
    You are a restaurant booking AI agent.

    User request:
    {messages[-1].content}

    Determine what the user wants.

    Possible intents:
    - search
    - recommendation
    - menu
    - reservation
    - cancellation
    - general_question
    """

    result = llm.invoke(prompt)

    return {
        "messages": messages,
        "intent": result.content,
        "response": result.content
    }


# -----------------------------
# 5. Graph
# -----------------------------

graph = StateGraph(RestaurantState)

graph.add_node("agent", agent_node)

graph.add_edge(START, "agent")
graph.add_edge("agent", END)

restaurant_agent = graph.compile()


# -----------------------------
# 6. Run
# -----------------------------

user_input = "Find an Italian restaurant for dinner."

result = restaurant_agent.invoke({
    "messages": [
        HumanMessage(content=user_input)
    ],
    "intent": "",
    "response": ""
})

print(result["response"])