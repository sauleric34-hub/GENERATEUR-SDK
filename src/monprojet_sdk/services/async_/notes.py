from typing import Awaitable, Optional
from .utils.to_async import to_async
from ..notes import NotesService
from ...net.sdk_config import SdkConfig
from ...models import Note


class NotesServiceAsync(NotesService):
    """
    Async Wrapper for NotesServiceAsync
    """

    def get_notes(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[None]:
        return to_async(super().get_notes)(request_config=request_config)

    def create_notes(
        self, request_body: Note, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[None]:
        return to_async(super().create_notes)(
            request_body, request_config=request_config
        )
