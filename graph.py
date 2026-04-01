from langgraph.graph import StateGraph, END
from state import PortfolioState

from tools.market_data_tool import fetch_stock_data
from tools.analytics_tool import compute_technical, compute_risk
from tools.memory_tool import load_memory, save_memory, update_memory

from agents.decision_agent import decision_agent
from agents.critic_agent import critic_agent
from agents.revision_agent import revision_agent


def load_memory_node(state: PortfolioState):
    state["portfolio_memory"] = load_memory()
    return state


def analytics_node(state: PortfolioState):

    df = fetch_stock_data(state["ticker"])
    state["technical_data"] = compute_technical(df)
    state["risk_data"] = compute_risk(df)

    return state


def decision_node(state: PortfolioState):

    user_input = f"""
Existing Portfolio:
{state["portfolio_memory"]["positions"]}

Technical Metrics:
{state["technical_data"]}

Risk Metrics:
{state["risk_data"]}
"""

    state["initial_decision"] = decision_agent.run(user_input)
    return state


def critic_node(state: PortfolioState):

    state["critique"] = critic_agent.run(
        f"Review this decision:\n\n{state['initial_decision']}"
    )
    return state


def revision_node(state: PortfolioState):

    state["final_decision"] = revision_agent.run(
        f"""
Original Decision:
{state['initial_decision']}

Critic Feedback:
{state['critique']}
"""
    )
    return state


def save_memory_node(state: PortfolioState):

    memory = update_memory(
        state["portfolio_memory"],
        state["ticker"],
        state.get("final_decision", state["initial_decision"])
    )

    save_memory(memory)
    return state


def should_revise(state: PortfolioState):
    if "Approval: NO" in state["critique"]:
        return "revise"
    return "final"


def build_graph():

    graph = StateGraph(PortfolioState)

    graph.add_node("load_memory", load_memory_node)
    graph.add_node("analytics", analytics_node)
    graph.add_node("decision", decision_node)
    graph.add_node("critic", critic_node)
    graph.add_node("revision", revision_node)
    graph.add_node("save_memory", save_memory_node)

    graph.set_entry_point("load_memory")

    graph.add_edge("load_memory", "analytics")
    graph.add_edge("analytics", "decision")
    graph.add_edge("decision", "critic")

    graph.add_conditional_edges(
        "critic",
        should_revise,
        {
            "revise": "revision",
            "final": "save_memory",
        }
    )

    graph.add_edge("revision", "save_memory")
    graph.add_edge("save_memory", END)

    return graph.compile()