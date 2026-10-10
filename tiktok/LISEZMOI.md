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
cd <dossier du repo ia-claude>
git fetch
git checkout tiktok-abondance
```

## 2. Dépose tes fichiers

- `tiktok/videos_sources/` → tes longues vidéos de nature (mp4, mov…)
- `tiktok/musique/` → tes musiques (mp3…), prises au hasard

Ces fichiers restent sur ton PC (ils ne sont pas envoyés sur GitHub).

Chaque vidéo utilise un passage de 10 s jamais montré, tous comptes confondus. À 9 vidéos par
jour, **1 heure de vidéo nature dure environ 40 jours**. Le script te prévient quand il faut en
rajouter.

## 3. Tes 3 comptes

Dans `tiktok/comptes.json`, remplace `compte1`, `compte2`, `compte3` par les vrais noms de tes
comptes. Chaque compte a son propre style pour qu'ils ne se ressemblent pas.

Les phrases sont dans `tiktok/banque_textes.json` (plus de 30 000 combinaisons). Tu peux en
ajouter toi-même, ou demander à Claude.

## 4. Générer les vidéos — 0 token

Le script écrit les textes et monte les vidéos tout seul, **sans Claude** :

```powershell
python .claude/skills/tiktok-abondance/scripts/generer.py
```

Résultat : `tiktok/a_publier/<date>/<compte>/video_1.mp4` … + `video_N_legende.txt`.

### Automatique chaque matin (toujours 0 token)

Planificateur de tâches Windows → **Créer une tâche de base** → Tous les jours, 8h →
Démarrer un programme :
- Programme : `python`
- Arguments : `.claude/skills/tiktok-abondance/scripts/generer.py`
- Commencer dans : `<dossier du repo>`

Claude (`/tiktok-abondance`) ne sert que pour modifier les phrases ou les comptes.

## 5. Publier (toi, sur ton téléphone)

Envoie les vidéos sur ton téléphone (Google Drive, câble…) et publie vers 12h, 18h et 21h,
en décalant d'environ 15 min d'un compte à l'autre. Copie la légende de `video_N_legende.txt`.

Avant de publier sur chaque compte, scrolle 10–15 min dans le « Pour toi » (likes, commentaires
dans la niche abondance) : c'est ce qui évite le shadowban.
