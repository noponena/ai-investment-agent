import os
from typing import Any, Dict, List

from dotenv import load_dotenv
import yaml

from .utils import find_project_root


class IOManager:
    def __init__(self, settings_file: str = "settings.yaml") -> None:
        self._keywords: List[str] = []
        self._buckets: List[Dict[str, str]] = []
        self.root_dir = find_project_root()
        self.config_dir = os.path.join(self.root_dir, "config")

        settings_path = (
            settings_file
            if os.path.isabs(settings_file)
            else os.path.join(self.config_dir, settings_file)
        )

        default_buckets_file = os.path.join(self.config_dir, "investment_buckets.yaml")
        load_dotenv(os.path.join(self.config_dir, ".env"), override=True)

        with open(settings_path, "r") as f:
            self.settings: Dict[str, Any] = yaml.safe_load(f)
        self._base_prompt: str = self.settings["base_prompt"].strip()
        # Use config/ path for bucket_file, unless overridden in settings
        bucket_file = self.settings.get("bucket_file", default_buckets_file)
        if not os.path.isabs(bucket_file):
            bucket_file = os.path.join(self.config_dir, bucket_file)
        self.bucket_file: str = bucket_file
        self._model: str = self.settings.get("model", "gpt-4o")

    @staticmethod
    def read_api_key(name: str) -> str:
        api_key = os.getenv(name)
        if not api_key:
            raise ValueError(f"'{name}' not found in environment variables.")
        return api_key

    @property
    def base_prompt(self) -> str:
        return self._base_prompt

    @property
    def buckets(self) -> List[Dict[str, str]]:
        if self._buckets:
            return self._buckets

        with open(self.bucket_file, "r") as f:
            data: Dict[str, Any] = yaml.safe_load(f)
        self._buckets = data["buckets"]
        return self._buckets

    @property
    def model(self) -> str:
        return self._model

    @property
    def keywords(self) -> List[str]:
        """
        Loads keywords from a text file, ignoring comments and blank lines.
        Caches the result for this instance.
        """
        if self._keywords:
            return self._keywords

        keyword_file = "filter_keywords.txt"
        path = keyword_file
        if not os.path.isabs(keyword_file):
            path = os.path.join(self.config_dir, keyword_file)
        with open(path, "r", encoding="utf-8") as f:
            self._keywords = [
                line.strip().lower()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
        return self._keywords
