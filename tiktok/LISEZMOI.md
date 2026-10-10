# TikTok abondance — installation sur Windows

## 1. Une seule fois

Ouvre **PowerShell** et lance :

```powershell
winget install Gyan.FFmpeg
winget install Python.Python.3.12
```

Ferme puis rouvre PowerShell, puis :

```powershell
pip install pillow
```

Récupère le skill :

```powershell
cd <dossier du repo ia-claude>
git pull
```

## 2. Dépose tes fichiers

- `tiktok/videos_sources/` → tes longues vidéos de nature (mp4, mov…)
- `tiktok/musique/` → tes musiques (mp3…). Les fichiers d'un dossier sont pris au hasard.

Ces fichiers restent sur ton PC (ils ne sont pas envoyés sur GitHub).

## 3. Générer les vidéos du jour

Dans Claude Code, ouvert dans le dossier du repo, tape :

```
/tiktok-abondance
```

Les 3 vidéos et leurs légendes arrivent dans `tiktok/a_publier/<date du jour>/`.

## 4. Automatique chaque matin

**Option simple** — Claude Code Desktop : crée une tâche planifiée quotidienne (ex. 8h) avec
le message `/tiktok-abondance`, dans le dossier du repo.

**Option Windows** — Planificateur de tâches → Créer une tâche de base → Tous les jours 8h →
Démarrer un programme :
- Programme : `powershell`
- Arguments : `-Command "cd '<dossier du repo>'; claude -p '/tiktok-abondance' --allowedTools 'Bash,Read,Write'"`

## 5. Publier

Envoie les vidéos sur ton téléphone (Google Drive, câble, etc.) et publie-les vers 12h, 18h et 21h
en copiant la légende de `video_N_legende.txt`.
