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

## Notes
- Assurez-vous que `ffmpeg` est installé pour les conversions si nécessaire.
- Utilisez des URL valides compatibles avec `yt-dlp`.
