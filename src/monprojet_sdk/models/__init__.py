from .etudiant import Etudiant
from .note import Note

# Rebuild models to resolve circular forward references
# This ensures Pydantic can properly validate models that reference each other
Etudiant.model_rebuild()
Note.model_rebuild()
