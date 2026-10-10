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

Chaque vidéo utilise un passage de 10 s jamais montré, tous comptes confondus. À 9 vidéos par
jour, **1 heure de vidéo nature dure environ 40 jours**. Le skill te prévient quand il faut en
rajouter.

## Tes 3 comptes

Ouvre `tiktok/comptes.json` et remplace `compte1`, `compte2`, `compte3` par les vrais noms de
tes comptes. Chaque compte a son propre style (couleurs, thèmes, mots à commenter, hashtags)
pour qu'ils ne se ressemblent pas. Tu peux aussi changer `videos_par_jour`.

## 3. Générer les vidéos du jour

Dans Claude Code, ouvert dans le dossier du repo, tape :

```
/tiktok-abondance
```

Les vidéos et leurs légendes arrivent dans `tiktok/a_publier/<date du jour>/<compte>/`
(3 par compte, donc 9 au total).

## 4. Automatique chaque matin

**Option simple** — Claude Code Desktop : crée une tâche planifiée quotidienne (ex. 8h) avec
le message `/tiktok-abondance`, dans le dossier du repo.

**Option Windows** — Planificateur de tâches → Créer une tâche de base → Tous les jours 8h →
Démarrer un programme :
- Programme : `powershell`
- Arguments : `-Command "cd '<dossier du repo>'; claude -p '/tiktok-abondance' --allowedTools 'Bash,Read,Write'"`

## 5. Publier

Envoie les vidéos sur ton téléphone (Google Drive, câble, etc.) et publie-les vers 12h, 18h et 21h (décale d'environ 15 min d'un compte à l'autre),
en copiant la légende de `video_N_legende.txt`.
