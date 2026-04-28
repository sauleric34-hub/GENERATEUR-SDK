import os
import subprocess
import sys
import time
import threading

def run_command(command, cwd=None):
    return subprocess.Popen(command, shell=True, cwd=cwd)

def main():
    print("="*60)
    print("🚀  DEMARRAGE DE L'ECOSYSTEME FULL-STACK  🚀")
    print("="*60)

    # 1. Génération
    print("\n[ETAPE 1] Génération du code (Front + Back)...")
    try:
        subprocess.check_call([sys.executable, "generate.py"])
        print("✅ Génération réussie !")
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de la génération.")
        return

    # 1b. Installation des dépendances
    print("\n[ETAPE 1b] Vérification des dépendances...")
    requirements = os.path.join("generated_backend", "requirements_backend.txt")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements])
        # On installe aussi requests pour le GUI
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "urllib3"])
        print("✅ Dépendances à jour !")
    except Exception as e:
        print(f"⚠️ Note: Erreur lors de l'auto-installation ({e}). Assurez-vous d'avoir pip installé.")

    # 2. Démarrage du Backend
    print("\n[ETAPE 2] Démarrage du Serveur API (HTTPS)...")
    backend_dir = "generated_backend"
    backend_script = "generated_app.py"
    
    # On utilise Popen pour ne pas bloquer
    backend_proc = run_command(f"{sys.executable} {backend_script}", cwd=backend_dir)
    
    print("⏳ Attente du démarrage du serveur (3s)...")
    time.sleep(3)

    # 3. Démarrage du Frontend (GUI)
    print("\n[ETAPE 3] Lancement de l'interface graphique (SDK)...")
    gui_script = "generated_gui.py"
    
    try:
        # Le GUI bloque jusqu'à sa fermeture
        subprocess.check_call([sys.executable, gui_script])
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur.")
    except Exception as e:
        print(f"Erreur GUI: {e}")
    finally:
        print("\nFermeture de l'écosystème...")
        backend_proc.terminate()
        print("👋 Au revoir !")

if __name__ == "__main__":
    main()
