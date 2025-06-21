import openai


def parse_response(response_text):
    results = []
    for line in response_text.splitlines():
        line = line.strip()
        if not line or "," not in line:
            continue  # skip empty or malformed lines
        try:
            bucket, ticker, name = [item.strip() for item in line.split(",", 2)]
            results.append({"bucket": bucket, "ticker": ticker, "name": name})
        except ValueError:
            continue  # skip lines that don’t split into 3
    return results


class OpenAIAgent:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def prompt_model(self, prompt, model):
        chat_completion = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return chat_completion.choices[0].message.content.strip()

    def get_recommendations(self, prompt, model):
        response = self.prompt_model(prompt, model)
        return parse_response(response)
