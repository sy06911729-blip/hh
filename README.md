# Téléchargeur vidéo (style IDM)

Application desktop simple pour télécharger des vidéos comme IDM, basée sur **yt-dlp** et **Tkinter**.

## Fonctionnalités
- File de téléchargements (ajout/suppression)
- Choix du dossier de sortie + ouverture rapide
- Modèle de nom de fichier personnalisable
- Sélection de qualité / format
- Limite de vitesse (optionnelle)
- Support des playlists (optionnel)
- Barre de progression et statut

## Prérequis
- Python 3.10+

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer l'application
```bash
python main.py
```

### Sur Windows
```powershell
python main.py
```

### Sur macOS / Linux
```bash
python3 main.py
```

## Créer un exécutable (Windows/macOS/Linux)
Installez PyInstaller, puis lancez le script de build:

```bash
pip install pyinstaller
python scripts/build_exe.py
```

Le binaire sera disponible dans le dossier `dist/` (ex: `dist/video-downloader`). 
Sur Windows, l'exécutable inclut des métadonnées (nom, version, copyright).

## Générer un exécutable via GitHub Actions
Vous pouvez produire automatiquement des exécutables via GitHub Actions (Windows/macOS/Linux).

1. Créez une étiquette (tag) `vX.Y.Z` sur le dernier commit, puis poussez-la:
```bash
git tag v0.1.0
git push origin v0.1.0
```
Astuce: pour voir vos tags locaux, utilisez `git tag -l`.
2. Téléchargez l'artefact généré dans l'onglet **Actions** de GitHub.

## Notes
- Assurez-vous que `ffmpeg` est installé pour les conversions si nécessaire.
- Utilisez des URL valides compatibles avec `yt-dlp`.
