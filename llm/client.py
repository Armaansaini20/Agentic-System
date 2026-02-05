import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # self.model_name = "gemini-3-flash-preview"
        # self.model_name = "gemini-2.5-flash"
        self.model_name = "gemini-2.5-flash-lite"

    def chat(self, messages, json_mode=False):
        system_instruction = ""
        user_content = ""

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                user_content += msg["content"] + "\n"

        # Safety: Gemini will error if user_content is empty
        if not user_content.strip():
            user_content = "Please process the previous instructions."

        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json" if json_mode else "text/plain"
        )

        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction
        )

        try:
            response = model.generate_content(user_content, generation_config=generation_config)
            if not response.text:
                return "{}" if json_mode else "I couldn't generate a response."
            return response.text
        except Exception as e:
            print(f"⚠️ Gemini API Error: {e}")
            return "{}" if json_mode else "Error: API call failed."