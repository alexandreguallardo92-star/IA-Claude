---
name: tiktok-abondance
description: Génère les 9 vidéos TikTok du jour (3 comptes × 3) de la niche « abondance positive », ou modifie les textes / comptes. Utilise ce skill quand l'utilisateur demande ses vidéos TikTok, « prépare mes tiktok », des vidéos abondance, ou veut changer les phrases, les comptes, les styles.
---

# TikTok « abondance positive »

**Économie de tokens : priorité absolue.** Ne lis aucun fichier, ne regarde aucune image,
n'ouvre pas l'historique. Tout est fait par le script.

## Générer les vidéos du jour

Depuis la racine du repo, une seule commande :

```
python .claude/skills/tiktok-abondance/scripts/generer.py
```

Puis réponds en une ligne : le dossier de sortie (dernière ligne du script) et les
avertissements éventuels (`⚠`). Rien d'autre.

## Modifier (seulement si l'utilisateur le demande)

- Phrases : `tiktok/banque_textes.json` (accroches, messages par thème, peur de rater, appels
  avec `{mot}`). Pour ajouter des phrases, n'ouvre que la partie concernée.
- Comptes : `tiktok/comptes.json` (nom, vidéos par jour, styles, thèmes, mots à commenter,
  légende, hashtags).
- Styles : `titre_vert` `titre_rouge` `titre_violet` `corps_blanc` `corps_bleu` `contour`
  `alerte_rouge` `appel_vert` `appel_jaune`. Pas d'emoji dans les blocs (seulement en légende).

Limites fixées avec l'utilisateur pour toute nouvelle phrase : pas de somme ni de date précise,
pas de menace qui fait peur (seulement la peur de rater une chance), jamais de demande d'argent,
de lien ou de coordonnées.
