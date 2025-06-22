from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests

from io_utils import IOManager


class ApiClientBase(ABC):
    _requires_api_key: bool = True

    def __init__(self, api_key: str = "", demo_mode: bool = False):
        self._io_manager = IOManager()
        self._api_key = api_key
        self._demo_mode = demo_mode
        self._request_timeout_seconds = 10

        needs_key = self._requires_api_key and not self._demo_mode
        if needs_key and not self._api_key:
            raise ValueError(f"{self.name} requires an API key.")

        if self._demo_mode:
            print(f"API client '{self.name}' is in demo mode!")
        self._init()

    def _send_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Generic method for sending HTTP requests.
        """
        try:
            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                timeout=self._request_timeout_seconds,
                **kwargs,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error fetching data from {self.name}: {e}")
            return None

    @abstractmethod
    def _init(self) -> None:
        """
        Unified API client initialization.
        """
        pass

    @property
    def name(self) -> str:
        if hasattr(self, "_name") and self._name:
            return self._name
        return self.__class__.__name__
