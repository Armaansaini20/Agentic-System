from llm.client import LLMClient

class VerifierAgent:
    def __init__(self):
        self.llm = LLMClient()

    def verify_and_respond(self, user_query, execution_results):
        prompt = f"""
        You are a Verifier Agent.
        Original Query: {user_query}
        Execution Results: {execution_results}
        
        1. Check if the results satisfy the query.
        2. If yes, generate a natural language final answer.
        3. If data is missing (e.g. error in results), explain what went wrong.
        
        Output JSON:
        {{
            "status": "success" or "failure",
            "final_answer": "Natural language response here."
        }}
        """
        response = self.llm.chat([{"role": "system", "content": prompt}], json_mode=True)
        return response