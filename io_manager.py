import yaml
import os
from dotenv import load_dotenv


class IOManager:
    def __init__(self, settings_file="settings.yaml"):
        load_dotenv()  # Load env vars from .env, if present
        with open(settings_file, "r") as f:
            self.settings = yaml.safe_load(f)
        self.base_prompt = self.settings["base_prompt"].strip()
        self.bucket_file = self.settings.get("bucket_file", "investment_buckets.yaml")
        self.model = self.settings.get("model", "gpt-4o")

    @staticmethod
    def read_api_key():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return api_key

    def read_base_prompt(self):
        return self.base_prompt

    def read_buckets(self):
        with open(self.bucket_file, "r") as f:
            data = yaml.safe_load(f)
        return data["buckets"]

    def get_model(self):
        return self.model
