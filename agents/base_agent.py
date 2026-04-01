from llm.model import call_llm


class BaseAgent:

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def run(self, user_input: str) -> str:

        prompt = f"""
{self.system_prompt}

{user_input}
"""
        return call_llm(prompt)