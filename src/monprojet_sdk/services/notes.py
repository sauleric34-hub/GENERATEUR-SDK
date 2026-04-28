from typing import Any, Optional
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import Note


class NotesService(BaseService):
    """
    Service class for NotesService operations.
    Provides methods to interact with NotesService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._get_notes_config: SdkConfig = {}
        self._create_notes_config: SdkConfig = {}

    def set_get_notes_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_notes.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_notes_config = config
        return self

    def set_create_notes_config(self, config: SdkConfig):
        """
        Sets method-level configuration for create_notes.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._create_notes_config = config
        return self

    @cast_models
    def get_notes(self, *, request_config: Optional[SdkConfig] = None) -> None:
        """get_notes

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        resolved_config = self._get_resolved_config(
            self._get_notes_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/notes",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        self.send_request(serialized_request)

    @cast_models
    def create_notes(
        self, request_body: Note, *, request_config: Optional[SdkConfig] = None
    ) -> None:
        """create_notes

        :param request_body: The request body.
        :type request_body: Note
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(Note).validate(request_body)

        resolved_config = self._get_resolved_config(
            self._create_notes_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/notes",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        self.send_request(serialized_request)
