from agents.base_agent import BaseAgent


revision_agent = BaseAgent(
    system_prompt="""
You are a senior portfolio manager.

If Approval is NO:
    Improve the decision.
If YES:
    Confirm it.

Return FINAL structured decision.
"""
)