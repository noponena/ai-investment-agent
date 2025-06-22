from typing import Dict, List

import openai

from .ai_agent import AIAgent


class OpenAIAgent(AIAgent):
    def __init__(self, api_key: str) -> None:
        self.client = openai.OpenAI(api_key=api_key)

    def prompt_model(self, prompt: str, model: str) -> str:
        chat_completion = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return chat_completion.choices[0].message.content.strip()

    def get_recommendations(self, prompt: str, model: str) -> List[Dict[str, str]]:
        response = self.prompt_model(prompt, model)
        return self.parse_response(response)

    def summarize_market_headlines(self, headlines: List[str], model: str = "gpt-4o") -> str:
        if not headlines:
            return "No current market headlines available."
        prompt = (
            "Summarize the following news headlines into a 3-sentence overview of global financial markets for investors. "
            "Focus on overall trends, not individual companies.\n\n"
            + "\n".join(f"- {h}" for h in headlines)
        )
        return self.prompt_model(prompt, model)

    @staticmethod
    def parse_response(response_text: str) -> List[Dict[str, str]]:
        results = []
        for line in response_text.splitlines():
            line = line.strip()
            if not line or "," not in line:
                continue
            try:
                bucket, ticker, name = [item.strip() for item in line.split(",", 2)]
                results.append({"bucket": bucket, "ticker": ticker, "name": name})
            except ValueError:
                continue
        return results
