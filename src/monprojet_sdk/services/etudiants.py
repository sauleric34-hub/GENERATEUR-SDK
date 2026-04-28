from typing import Any, Optional, List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import Etudiant


class EtudiantsService(BaseService):
    """
    Service class for EtudiantsService operations.
    Provides methods to interact with EtudiantsService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._get_etudiants_config: SdkConfig = {}
        self._create_etudiants_config: SdkConfig = {}

    def set_get_etudiants_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_etudiants.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_etudiants_config = config
        return self

    def set_create_etudiants_config(self, config: SdkConfig):
        """
        Sets method-level configuration for create_etudiants.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._create_etudiants_config = config
        return self

    @cast_models
    def get_etudiants(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> List[Etudiant]:
        """get_etudiants

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: List[Etudiant]
        """

        resolved_config = self._get_resolved_config(
            self._get_etudiants_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/etudiants",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return [Etudiant.model_validate(item) for item in response]

    @cast_models
    def create_etudiants(
        self, request_body: Etudiant, *, request_config: Optional[SdkConfig] = None
    ) -> None:
        """create_etudiants

        :param request_body: The request body.
        :type request_body: Etudiant
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(Etudiant).validate(request_body)

        resolved_config = self._get_resolved_config(
            self._create_etudiants_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/etudiants",
                [],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        self.send_request(serialized_request)
