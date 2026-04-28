from monprojet_sdk import MonprojetSdk

sdk = MonprojetSdk(timeout=10000)

result = sdk.etudiants.get_etudiants()

print(result)
