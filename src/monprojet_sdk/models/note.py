from pydantic import Field
from typing import Optional
from .utils.base_model import BaseModel


class Note(BaseModel):
    """Note

    :param id_: id_, defaults to None
    :type id_: int, optional
    :param valeur: valeur
    :type valeur: float
    :param matiere: matiere
    :type matiere: str
    :param etudiant_id: etudiant_id, defaults to None
    :type etudiant_id: int, optional
    """

    id_: Optional[int] = Field(alias="id", serialization_alias="id", default=None)
    valeur: float
    matiere: str
    etudiant_id: Optional[int] = Field(default=None)
