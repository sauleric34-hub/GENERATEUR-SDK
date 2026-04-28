from typing import Union
from .services.etudiants import EtudiantsService
from .services.notes import NotesService
from .net.environment import Environment


class MonprojetSdk:
    """
    Main SDK client class for MonprojetSdk.
    Provides centralized configuration and access to all service endpoints.
    Supports authentication, environment management, and global timeout settings.
    """

    def __init__(
        self, base_url: Union[Environment, str, None] = None, timeout: int = 60000
    ):
        """
        Initializes MonprojetSdk the SDK class.
        """

        _resolved_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self._base_url = _resolved_url.rstrip("/") if _resolved_url else _resolved_url
        self.etudiants = EtudiantsService(base_url=self._base_url)
        self.notes = NotesService(base_url=self._base_url)
        self.set_timeout(timeout)

    def set_base_url(self, base_url: Union[Environment, str]):
        """
        Sets the base URL for the entire SDK.

        :param Union[Environment, str] base_url: The base URL to be set.
        :return: The SDK instance.
        """
        _resolved_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self._base_url = _resolved_url.rstrip("/") if _resolved_url else _resolved_url

        self.etudiants.set_base_url(self._base_url)
        self.notes.set_base_url(self._base_url)

        return self

    def set_timeout(self, timeout: int):
        """
        Sets the timeout for the entire SDK.

        :param int timeout: The timeout (ms) to be set.
        :return: The SDK instance.
        """
        self.etudiants.set_timeout(timeout)
        self.notes.set_timeout(timeout)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
