from ai_agent import OpenAIAgent
from io_manager import IOManager


def main():
    io = IOManager()
    api_key = io.read_api_key("OPENAI_API_KEY")
    base_prompt = io.read_base_prompt()
    buckets = io.read_buckets()
    model = io.get_model()
    print(f"Using model: {model}")

    prompt = base_prompt + "\n\nBuckets and descriptions:\n"
    for b in buckets:
        prompt += f"{b['name']} ({b['allocation']}%): {b['description']}\n"

    print(f"Prompt sent to AI:\n\n{prompt}")

    agent = OpenAIAgent(api_key)
    recommendations = agent.get_recommendations(prompt, model=model)

    print("AI's response:\n")
    for rec in recommendations:
        print(f"{rec['bucket']}: {rec['ticker']} – {rec['name']}")


if __name__ == "__main__":
    main()
