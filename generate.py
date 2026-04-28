import os
import subprocess
import sys

def main():
    # Paths relative to the project root
    spec_path = os.path.join("..", "app_api_finale", "openapi.yaml")
    
    # Frontend config
    gui_output_path = "generated_gui.py"
    gui_generator_script = "gui_generator.py"

    # Backend config
    backend_output_dir = "generated_backend"
    backend_generator_script = "backend_generator.py"

    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found at {spec_path}")
        return

    # 1. Generate Frontend
    print(f"--- Generating Frontend (Tkinter) ---")
    try:
        subprocess.check_call([sys.executable, gui_generator_script, spec_path, gui_output_path])
        print(f"Frontend generated: {gui_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Frontend generation: {e}")

    # 2. Generate Backend
    print(f"\n--- Generating Backend (Flask) ---")
    try:
        subprocess.check_call([sys.executable, backend_generator_script, spec_path, backend_output_dir])
        print(f"Backend generated in: {backend_output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Backend generation: {e}")

    print("\n" + "="*40)
    print("SUCCESS: Full Stack Ecosystem Generated!")
    print("="*40)
    print(f"To start the server: cd {backend_output_dir} && python generated_app.py")
    print(f"To start the GUI: python {gui_output_path}")

if __name__ == "__main__":
    main()
