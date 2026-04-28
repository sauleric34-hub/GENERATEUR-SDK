# EtudiantsService

A list of all methods in the `EtudiantsService` service. Click on the method name to view detailed information about that method.

| Methods                               | Description |
| :------------------------------------ | :---------- |
| [get_etudiants](#get_etudiants)       |             |
| [create_etudiants](#create_etudiants) |             |

## get_etudiants

- HTTP Method: `GET`
- Endpoint: `/etudiants`

**Return Type**

`List[Etudiant]`

**Example Usage Code Snippet**

```python
from monprojet_sdk import MonprojetSdk

sdk = MonprojetSdk(
    timeout=10000
)

result = sdk.etudiants.get_etudiants()

print(result)
```

## create_etudiants

- HTTP Method: `POST`
- Endpoint: `/etudiants`

**Parameters**

| Name         | Type                              | Required | Description       |
| :----------- | :-------------------------------- | :------- | :---------------- |
| request_body | [Etudiant](../models/Etudiant.md) | ✅       | The request body. |

**Example Usage Code Snippet**

```python
from monprojet_sdk import MonprojetSdk
from monprojet_sdk.models import Etudiant

sdk = MonprojetSdk(
    timeout=10000
)

request_body = Etudiant(
    id_=8,
    nom="nom",
    filiere="filiere"
)

result = sdk.etudiants.create_etudiants(request_body=request_body)

print(result)
```
