# MonprojetSdk Python SDK 1.0.0<a id="monprojetsdk-python-sdk-100"></a>

Welcome to the MonprojetSdk SDK documentation. This guide will help you get started with integrating and using the MonprojetSdk SDK in your project.

## Versions<a id="versions"></a>

- SDK version: `1.0.0`

## About the API<a id="about-the-api"></a>

API centralisée pour la gestion des notes, la sécurité et la détection de billets.

## Table of Contents<a id="table-of-contents"></a>

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Setting a Custom Timeout](#setting-a-custom-timeout)
- [Sample Usage](#sample-usage)
- [Services](#services)
- [Models](#models)

# Setup & Configuration<a id="setup--configuration"></a>

## Supported Language Versions<a id="supported-language-versions"></a>

This SDK is compatible with the following versions: `Python >= 3.7`

## Installation<a id="installation"></a>

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install monprojet_sdk
```

If you are using Python 3, you can use `pip3` instead:

```bash
pip3 install monprojet_sdk
```

## Setting a Custom Timeout<a id="setting-a-custom-timeout"></a>

You can set a custom timeout for the SDK's HTTP requests as follows:

```py
from monprojet_sdk import MonprojetSdk

sdk = MonprojetSdk(timeout=10000)
```

# Sample Usage<a id="sample-usage"></a>

Below is a comprehensive example demonstrating how to authenticate and call a simple endpoint:

```py
from monprojet_sdk import MonprojetSdk

sdk = MonprojetSdk(
    timeout=10000
)

result = sdk.etudiants.get_etudiants()

print(result)

```

# Async Usage<a id="async-usage"></a>

The SDK includes an Async Client for making asynchronous API requests. This is useful for applications that need non-blocking operations, like web servers or apps with a graphical user interface.

```py
import asyncio
from monprojet_sdk import MonprojetSdkAsync

sdk = MonprojetSdkAsync(
    timeout=10000
)


async def main():
  result = await sdk.etudiants.get_etudiants()
  print(result)

asyncio.run(main())
```

## Services<a id="services"></a>

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services:</summary>

| Name      |
| :-------- |
| etudiants |
| notes     |

</details>

## Models<a id="models"></a>

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models:</summary>

| Name     | Description |
| :------- | :---------- |
| Etudiant |             |
| Note     |             |

</details>
