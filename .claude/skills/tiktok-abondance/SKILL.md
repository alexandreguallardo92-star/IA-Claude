---
name: tiktok-abondance
description: Prépare les vidéos TikTok du jour pour le compte « abondance positive » (niche manifestation / loi de l'attraction) — écrit les textes, coupe un passage au hasard des rushs nature, pose les blocs de texte colorés, ajoute la musique et range tout dans tiktok/a_publier/. Utilise ce skill dès que l'utilisateur demande les vidéos TikTok du jour, des vidéos abondance, « prépare mes tiktok », ou quand la tâche planifiée quotidienne se lance.
---

# TikTok « abondance positive »

Objectif actuel : **atteindre 10 000 abonnés** (condition du programme de rémunération TikTok)
sur **3 comptes**, avec **au moins 3 vidéos par jour et par compte** (9 vidéos par jour),
**10 secondes maximum**, et **toutes différentes**. Étape suivante (plus tard) : vidéos de plus
d'une minute pour être rémunéré.

## Dossiers (à la racine du repo)

- `tiktok/videos_sources/` — longues vidéos de nature fournies par l'utilisateur
- `tiktok/musique/` — musiques fournies par l'utilisateur (mp3, m4a, wav…)
- `tiktok/comptes.json` — les comptes : nom, nombre de vidéos par jour, styles, thèmes,
  mots à commenter, légende et hashtags propres à chacun
- `tiktok/a_publier/AAAA-MM-JJ/<compte>/` — résultat : `video_N.mp4` + `video_N_legende.txt`
- `tiktok/historique.json` — tout ce qui a déjà été publié, tous comptes confondus
  (compte, textes, rush, moment coupé)

## Déroulé

1. **Vérifier** qu'il y a au moins une vidéo dans `tiktok/videos_sources/`. Sinon, s'arrêter et
   demander à l'utilisateur d'en déposer. S'il n'y a pas de musique, prévenir mais continuer.
2. **Lire `tiktok/comptes.json`** et **`tiktok/historique.json`** (s'il existe). Aucun texte ne
   doit être répété, ni sur le même compte, ni d'un compte à l'autre.
3. **Pour chaque compte**, écrire ses `videos_par_jour` vidéos dans un fichier JSON temporaire
   (format et règles plus bas) en respectant **son identité** : ses styles, ses thèmes, ses mots à
   commenter, sa légende et ses hashtags. Les comptes ne doivent pas se ressembler entre eux.
4. **Lancer le montage** pour chaque compte, depuis la racine du repo :
   ```
   python .claude/skills/tiktok-abondance/scripts/generer.py <fichier.json> --compte <nom>
   ```
   Le script choisit un rush au hasard, le coupe à un moment au hasard (10 s) qui n'a jamais
   servi (aucun compte ne réutilise les mêmes images), le recadre en 1080×1920, pose les blocs
   de texte, ajoute une musique au hasard (départ au hasard, fondus) et met à jour l'historique.
5. **Contrôler** une image de chaque vidéo (`ffmpeg -ss 3 -i video_N.mp4 -frames:v 1 apercu.png`)
   : texte lisible, rien de coupé. Supprimer l'aperçu ensuite.
6. **Résumer** à l'utilisateur, compte par compte : chemin du dossier, les textes, les légendes
   à copier. Rappeler les heures conseillées : ~12h, ~18h, ~21h, en décalant d'environ
   15 minutes d'un compte à l'autre. Si le script a prévenu que les rushs s'épuisent,
   le dire clairement.

## Format du JSON

```json
[
  {
    "blocs": [
      {"texte": "FÉLICITATIONS !", "style": "titre_rouge"},
      {"texte": "Une grosse, très grosse somme d'argent est en train d'arriver vers toi", "style": "corps_bleu"},
      {"texte": "Mais si tu ignores ce message, tu passeras à côté", "style": "alerte_rouge"},
      {"texte": "Clique sur le + et commente \"argent\"", "style": "appel_vert"}
    ],
    "legende": "abonne-toi pour recevoir l'abondance 🔮 #abondance #abondancepositive #loidelattraction #manifestation #argent"
  }
]
```

Styles disponibles :
- Titre : `titre_vert`, `titre_rouge`, `titre_violet`
- Corps : `corps_blanc`, `corps_bleu`, `contour` (texte blanc contour noir, sans fond)
- Avertissement : `alerte_rouge`
- Appel à l'action : `appel_vert`, `appel_jaune`

Pas d'emoji dans les blocs (la police ne les affiche pas) — les emojis vont dans la légende.

## Règles d'écriture

Structure qui marche dans la niche (3 à 4 blocs, lisible en 10 s) :
1. **Accroche** courte en gros : FÉLICITATIONS ! / URGENT ! / CE N'EST PAS UN HASARD / STOP ! / LIS ÇA
2. **Le message** : l'abondance, l'argent, la chance, une bonne nouvelle qui arrive vers la personne
3. **Peur de rater** (optionnel) : « si tu ignores ce message, tu passeras à côté »,
   « ne laisse pas passer cette chance », « cette vidéo ne reviendra pas »
4. **Appel à l'action**, toujours présent : « Clique sur le + et commente "argent" »,
   « Abonne-toi et commente "je reçois" », « Clique sur le + et écris "merci" »

Varier : l'accroche, la couleur des blocs, le mot à commenter (argent, je veux, je reçois, merci,
amen, abondance, oui, c'est pour moi…), le thème (argent, chance, amour, santé, travail, famille).

Limites fixées avec l'utilisateur :
- **Pas de somme précise ni de date précise** (« 6 chiffres lundi 7 avril ») — rester vague :
  « une grosse somme », « bientôt », « cette semaine ».
- **Pas de menace qui fait peur** (« ça peut être grave », « il t'arrivera malheur ») —
  uniquement la peur de rater une chance.
- Ne jamais demander d'argent, de lien, de coordonnées.

Légende : une phrase « abonne-toi pour… » + 4 à 6 hashtags parmi #abondance #abondancepositive
#loidelattraction #manifestation #argent #chance #spiritualité #affirmationpositive #pourtoi.
