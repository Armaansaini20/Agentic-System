import json
from llm.client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_query, tools_definitions):
        prompt = f"""
        You are a Planner Agent.
        User Query: {user_query}
        Available Tools: {json.dumps(tools_definitions)}
        
        Create a JSON plan with a list of steps. Each step must use a tool or be a reasoning step.
        Format:
        {{
            "steps": [
                {{"tool": "tool_name", "args": {{...}}, "reason": "why I need this"}}
            ]
        }}
        """
        response = self.llm.chat([{"role": "system", "content": prompt}], json_mode=True)
        return json.loads(response)