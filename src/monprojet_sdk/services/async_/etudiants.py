from typing import Awaitable, Optional, List
from .utils.to_async import to_async
from ..etudiants import EtudiantsService
from ...net.sdk_config import SdkConfig
from ...models import Etudiant


class EtudiantsServiceAsync(EtudiantsService):
    """
    Async Wrapper for EtudiantsServiceAsync
    """

    def get_etudiants(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[List[Etudiant]]:
        return to_async(super().get_etudiants)(request_config=request_config)

    def create_etudiants(
        self, request_body: Etudiant, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[None]:
        return to_async(super().create_etudiants)(
            request_body, request_config=request_config
        )
