# API Full-Stack Generator (Academic Edition)

This tool generates a complete REST API ecosystem (Backend + Frontend) from an OpenAPI 3.0 specification, following the academic principles taught in the Keyce B2 course.

## Standards Followed

- **HTTPS (SSL)**: Communication is secured via HTTPS using self-signed (adhoc) certificates.
- **RFC 7807**: Errors are returned in the `application/problem+json` format.
- **HATEOAS**: The API includes navigation links in its responses (see `/api/v1/health`).
- **API Versioning**: All endpoints are prefixed with `/api/v1`.
- **JWT Auth**: Stateless authentication with JSON Web Tokens and role-based placeholders.
- **Persistence**: Automated SQLite database generation based on OpenAPI schemas.

## Comment tout lancer en UN CLIC (Interface Graphique)

J'ai créé une interface dédiée pour piloter le générateur. Pour l'utiliser :
1. Allez dans le dossier `SDKGENERATION`.
2. Lancez le contrôleur :
   ```bash
   python SDK_GENERATOR_GUI.py
   ```
3. Parcourez votre fichier `openapi.yaml` et cliquez sur **GÉNÉRER & LANCER**.

L'outil s'occupera de tout : génération du code, installation des dépendances, démarrage du serveur HTTPS (ACID) et lancement de l'interface client.

## Project Structure

- `gui_generator.py`: Generates the Tkinter client.
- `backend_generator.py`: Generates the Flask server and SQLite DB.
- `generate.py`: Main entry point for full-stack generation.
