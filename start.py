#!/usr/bin/env python3
"""
Script de démarrage pour l'application ISIC
Lance le backend FastAPI et ouvre le frontend
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

def main():
    """
    Fonction principale pour démarrer l'application
    """
    print("🚀 Démarrage de l'application ISIC...")

    # Vérifier que nous sommes dans le bon répertoire
    base_dir = Path(__file__).parent
    backend_dir = base_dir / "backend"
    web_dir = base_dir / "web"

    if not backend_dir.exists():
        print("❌ Dossier backend introuvable")
        return

    if not web_dir.exists():
        print("❌ Dossier web introuvable")
        return

    print("📦 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=base_dir, check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Avertissement: Erreur lors de l'installation des dépendances")

    print("🌐 Démarrage du backend FastAPI sur http://127.0.0.1:8000...")
    
    backend_process = None
    frontend_process = None
    
    try:
        # Démarrer le backend depuis le répertoire backend
        os.chdir(backend_dir)
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Backend démarré")

        # Attendre que le backend démarre
        time.sleep(2)

        # Démarrer un serveur HTTP pour le frontend
        print("📁 Démarrage du serveur web frontend sur http://127.0.0.1:3000...")
        os.chdir(web_dir)
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "http.server",
            "3000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Frontend démarré")

        # Attendre que le frontend démarre
        time.sleep(2)

        # Ouvrir l'application dans le navigateur
        frontend_url = "http://127.0.0.1:3000"
        print(f"🎨 Ouverture du navigateur: {frontend_url}")
        webbrowser.open(frontend_url)

        print("\n" + "="*50)
        print("✅ Application ISIC démarrée avec succès!")
        print("="*50)
        print(f"🌐 Frontend:        {frontend_url}")
        print(f"📊 API:             http://127.0.0.1:8000")
        print(f"📚 API Docs:        http://127.0.0.1:8000/docs")
        print("="*50)
        print("Appuyez sur Ctrl+C pour arrêter l'application...")
        print("="*50 + "\n")

        # Garder le script en cours d'exécution
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("⚠️ Le backend s'est arrêté")
                break
            if frontend_process.poll() is not None:
                print("⚠️ Le frontend s'est arrêté")
                break

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt de l'application...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        # Arrêter les processus
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("👋 Application arrêtée")

if __name__ == "__main__":
    main()