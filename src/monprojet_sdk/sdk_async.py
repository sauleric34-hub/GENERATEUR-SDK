from typing import Union
from .net.environment import Environment
from .sdk import MonprojetSdk
from .services.async_.etudiants import EtudiantsServiceAsync
from .services.async_.notes import NotesServiceAsync


class MonprojetSdkAsync(MonprojetSdk):
    """
    MonprojetSdkAsync is the asynchronous version of the MonprojetSdk SDK Client.
    """

    def __init__(
        self, base_url: Union[Environment, str, None] = None, timeout: int = 60000
    ):
        super().__init__(base_url=base_url, timeout=timeout)

        self.etudiants = EtudiantsServiceAsync(base_url=self._base_url)
        self.notes = NotesServiceAsync(base_url=self._base_url)
