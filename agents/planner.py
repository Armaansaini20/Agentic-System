import json
from llm.client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_query, tools_definitions):
        prompt = f"""
        You are an expert Planner Agent. Your goal is to break down the user query into steps.
        
        CRITICAL: Identify steps that can be executed in PARALLEL. 
        - If two tool calls do not depend on each other's output, mark them as "parallel": true.
        - If a step needs data from a previous tool, mark it "parallel": false.

        User Query: {user_query}
        Available Tools: {json.dumps(tools_definitions)}
        
        Format the output as a clean JSON object:
        {{
            "steps": [
                {{
                    "tool": "tool_name", 
                    "args": {{...}}, 
                    "parallel": true, 
                    "reason": "why I need this"
                }}
            ]
        }}
        """
        # Call LLM with JSON mode
        response = self.llm.chat([{"role": "system", "content": prompt}], json_mode=True)
        
        # --- FIX START: Handle different response types ---
        if hasattr(response, 'text'):
            # It's a full response object (Gemini SDK style)
            plan_text = response.text
            usage = getattr(response, 'usage_metadata', None)
        else:
            # It's already a string (LLMClient might have pre-extracted .text)
            plan_text = response
            usage = None 

        # Clean up potential markdown formatting that breaks json.loads
        plan_text = plan_text.replace("```json", "").replace("```", "").strip()
        
        try:
            plan_data = json.loads(plan_text)
        except json.JSONDecodeError as e:
            # Fallback for common LLM parsing errors
            print(f"❌ JSON Parsing Error: {e}")
            plan_data = {"steps": [], "error": "Failed to parse AI plan"}
        # --- FIX END ---
        
        return plan_data, usage