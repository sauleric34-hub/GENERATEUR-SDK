# NotesService

A list of all methods in the `NotesService` service. Click on the method name to view detailed information about that method.

| Methods                       | Description |
| :---------------------------- | :---------- |
| [get_notes](#get_notes)       |             |
| [create_notes](#create_notes) |             |

## get_notes

- HTTP Method: `GET`
- Endpoint: `/notes`

**Example Usage Code Snippet**

```python
from monprojet_sdk import MonprojetSdk

sdk = MonprojetSdk(
    timeout=10000
)

result = sdk.notes.get_notes()

print(result)
```

## create_notes

- HTTP Method: `POST`
- Endpoint: `/notes`

**Parameters**

| Name         | Type                      | Required | Description       |
| :----------- | :------------------------ | :------- | :---------------- |
| request_body | [Note](../models/Note.md) | ✅       | The request body. |

**Example Usage Code Snippet**

```python
from monprojet_sdk import MonprojetSdk
from monprojet_sdk.models import Note

sdk = MonprojetSdk(
    timeout=10000
)

request_body = Note(
    id_=2,
    valeur=8.44,
    matiere="matiere",
    etudiant_id=8
)

result = sdk.notes.create_notes(request_body=request_body)

print(result)
```
