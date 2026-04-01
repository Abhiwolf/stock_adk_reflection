from typing import TypedDict, Dict, Any


class PortfolioState(TypedDict, total=False):
    ticker: str
    technical_data: Dict[str, Any]
    risk_data: Dict[str, Any]
    portfolio_memory: Dict[str, Any]
    initial_decision: str
    critique: str
    final_decision: str