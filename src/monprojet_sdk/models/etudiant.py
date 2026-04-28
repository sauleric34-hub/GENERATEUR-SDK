from pydantic import Field
from typing import Optional
from .utils.base_model import BaseModel


class Etudiant(BaseModel):
    """Etudiant

    :param id_: id_, defaults to None
    :type id_: int, optional
    :param nom: nom
    :type nom: str
    :param filiere: filiere
    :type filiere: str
    """

    id_: Optional[int] = Field(alias="id", serialization_alias="id", default=None)
    nom: str
    filiere: str
