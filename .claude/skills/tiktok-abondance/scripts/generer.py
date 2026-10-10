"""Génère les vidéos TikTok « abondance positive » du jour, pour tous les comptes.

Usage :
    python generer.py [--racine DOSSIER] [--duree 10] [--compte NOM]

Sans appel à Claude : les textes sont tirés de tiktok/banque_textes.json selon
l'identité de chaque compte (tiktok/comptes.json), sans jamais répéter un texte
déjà publié. Pour chaque vidéo, un rush de videos_sources/ est coupé à un moment
jamais utilisé, recadré en 1080x1920, les blocs de texte sont posés dessus et une
musique de musique/ est ajoutée. Sortie : a_publier/AAAA-MM-JJ/<compte>/.
"""

import argparse
import datetime
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

LARGEUR, HAUTEUR = 1080, 1920
EXT_VIDEO = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v")
EXT_AUDIO = (".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac")

# Styles repris des vidéos de la niche : blocs pleins, coins arrondis.
STYLES = {
    "titre_vert":   {"fond": (102, 187, 72),  "texte": (255, 255, 255), "taille": 120},
    "titre_rouge":  {"fond": (235, 64, 52),   "texte": (255, 255, 255), "taille": 110},
    "titre_violet": {"fond": (170, 170, 255), "texte": (55, 50, 190),   "taille": 120},
    "corps_blanc":  {"fond": (255, 255, 255), "texte": (0, 0, 0),       "taille": 68},
    "corps_bleu":   {"fond": (20, 140, 255),  "texte": (255, 255, 255), "taille": 64},
    "alerte_rouge": {"fond": (235, 64, 52),   "texte": (255, 255, 255), "taille": 66},
    "appel_vert":   {"fond": (20, 170, 40),   "texte": (255, 255, 255), "taille": 66},
    "appel_jaune":  {"fond": (255, 245, 170), "texte": (120, 90, 20),   "taille": 66},
    "contour":      {"fond": None,            "texte": (255, 255, 255), "taille": 72},
}

POLICES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def police(taille):
    for chemin in POLICES:
        if os.path.exists(chemin):
            return ImageFont.truetype(chemin, taille)
    return ImageFont.load_default(taille)


def lister(dossier, extensions):
    if not os.path.isdir(dossier):
        return []
    return sorted(
        os.path.join(dossier, f)
        for f in os.listdir(dossier)
        if f.lower().endswith(extensions)
    )


def duree(fichier):
    sortie = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", fichier],
        capture_output=True, text=True, check=True,
    )
    return float(sortie.stdout.strip())


def couper_lignes(texte, fnt, largeur_max):
    """Découpe le texte pour qu'aucune ligne ne dépasse largeur_max pixels."""
    # Espace insécable devant la ponctuation française : « ! » ne part jamais seul à la ligne.
    for signe in "!?:;":
        texte = texte.replace(f" {signe}", f"\u00a0{signe}")
    mots, lignes, ligne = [m for m in texte.split(" ") if m], [], ""
    for mot in mots:
        essai = f"{ligne} {mot}".strip()
        if fnt.getlength(essai) <= largeur_max or not ligne:
            ligne = essai
        else:
            lignes.append(ligne)
            ligne = mot
    if ligne:
        lignes.append(ligne)
    return lignes


def rendre_bloc(bloc):
    style = STYLES.get(bloc.get("style"), STYLES["corps_blanc"])
    taille = style["taille"]
    marge, interligne = 40, int(taille * 0.22)
    largeur_max = LARGEUR - 2 * 60 - 2 * marge
    fnt = police(taille)
    lignes = couper_lignes(bloc["texte"], fnt, largeur_max)
    # Réduit la police si le bloc est trop haut ou si un mot seul dépasse.
    while (len(lignes) > 7 or max(fnt.getlength(l) for l in lignes) > largeur_max) and taille > 40:
        taille -= 4
        fnt = police(taille)
        lignes = couper_lignes(bloc["texte"], fnt, largeur_max)

    hauteur_ligne = fnt.getbbox("ÉgjpqyÀ")[3]
    larg_texte = max(int(fnt.getlength(l)) for l in lignes)
    larg = larg_texte + 2 * marge
    pad_v = int(marge * 0.6)
    haut = len(lignes) * hauteur_ligne + (len(lignes) - 1) * interligne + 2 * pad_v
    img = Image.new("RGBA", (larg, haut), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if style["fond"]:
        d.rounded_rectangle([0, 0, larg - 1, haut - 1], radius=18, fill=style["fond"] + (255,))
    y = pad_v
    for l in lignes:
        x = (larg - fnt.getlength(l)) / 2
        if style["fond"] is None:
            d.text((x, y), l, font=fnt, fill=style["texte"],
                   stroke_width=6, stroke_fill=(0, 0, 0))
        else:
            d.text((x, y), l, font=fnt, fill=style["texte"])
        y += hauteur_ligne + interligne
    return img


def rendre_calque(blocs, chemin):
    """Empile les blocs verticalement, centrés, comme dans les vidéos de la niche."""
    images = [rendre_bloc(b) for b in blocs]
    espace = 90
    total = sum(i.height for i in images) + espace * (len(images) - 1)
    calque = Image.new("RGBA", (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    # Centré un peu au-dessus du milieu pour laisser la place à la légende TikTok.
    y = max(200, (HAUTEUR - total) // 2 - 120)
    for i in images:
        calque.alpha_composite(i, ((LARGEUR - i.width) // 2, y))
        y += i.height + espace
    calque.save(chemin)


def choisir_passage(sources, historique, duree_clip):
    """Prend un rush et un moment au hasard qui ne recoupe aucun passage déjà utilisé,
    tous comptes confondus : deux vidéos ne montrent jamais les mêmes images."""
    deja = {}
    for h in historique:
        deja.setdefault(h["source"], []).append(h["debut_source"])
    for _ in range(200):
        source = random.choice(sources)
        d_src = duree(source)
        debut = random.uniform(0, max(0.0, d_src - duree_clip))
        if all(abs(debut - d) >= duree_clip for d in deja.get(os.path.basename(source), [])):
            return source, debut
    print("⚠ Rushs presque épuisés : ajoute de nouvelles vidéos dans videos_sources/.")
    return source, debut


def generer_video(source, debut, musique, calque, sortie, duree_clip):
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-ss", f"{debut:.2f}", "-t", str(duree_clip), "-i", source,
           "-i", calque]
    filtre = (
        f"[0:v]scale={LARGEUR}:{HAUTEUR}:force_original_aspect_ratio=increase,"
        f"crop={LARGEUR}:{HAUTEUR},setsar=1,fps=30[fond];"
        f"[fond][1:v]overlay=0:0[v]"
    )
    cartes = ["-map", "[v]"]
    if musique:
        d_mus = duree(musique)
        debut_mus = random.uniform(0, max(0.0, d_mus - duree_clip))
        cmd += ["-ss", f"{debut_mus:.2f}", "-t", str(duree_clip), "-i", musique]
        filtre += (
            f";[2:a]afade=t=in:d=0.5,afade=t=out:st={duree_clip - 1}:d=1[a]"
        )
        cartes += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-filter_complex", filtre, *cartes,
            "-t", str(duree_clip),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", sortie]
    subprocess.run(cmd, check=True)


def ecrire_texte(compte, banque, deja_vus, messages_du_compte):
    """Compose une vidéo à partir de la banque, sans répéter un texte déjà publié."""
    messages = [m for t in compte["themes"] for m in banque["messages"].get(t, [])]
    # Priorité aux messages que ce compte n'a pas encore utilisés.
    neufs = [m for m in messages if m not in messages_du_compte] or messages
    for _ in range(500):
        blocs = [
            {"texte": random.choice(banque["accroches"]), "style": random.choice(compte["styles_titre"])},
            {"texte": random.choice(neufs), "style": random.choice(compte["styles_corps"])},
        ]
        if random.random() < 0.6:
            blocs.append({"texte": random.choice(banque["peur_de_rater"]), "style": "alerte_rouge"})
        appel = random.choice(banque["appels"]).format(mot=random.choice(compte["mots_a_commenter"]))
        blocs.append({"texte": appel, "style": random.choice(compte["styles_appel"])})
        cle = tuple(b["texte"] for b in blocs)
        if cle not in deja_vus:
            break
    deja_vus.add(cle)
    messages_du_compte.add(blocs[1]["texte"])
    legende = compte["legende"] + " " + " ".join(random.sample(compte["hashtags"], min(5, len(compte["hashtags"]))))
    return {"blocs": blocs, "legende": legende}


def main():
    ici = os.path.dirname(os.path.abspath(__file__))
    racine_defaut = os.path.abspath(os.path.join(ici, "..", "..", "..", "..", "tiktok"))
    p = argparse.ArgumentParser()
    p.add_argument("--racine", default=racine_defaut)
    p.add_argument("--duree", type=float, default=10)
    p.add_argument("--compte", help="ne générer que pour ce compte")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg introuvable : installe-le (winget install Gyan.FFmpeg) puis relance le terminal.")

    with open(os.path.join(args.racine, "comptes.json"), encoding="utf-8") as f:
        comptes = json.load(f)
    with open(os.path.join(args.racine, "banque_textes.json"), encoding="utf-8") as f:
        banque = json.load(f)
    if args.compte:
        comptes = [c for c in comptes if c["nom"] == args.compte]

    sources = lister(os.path.join(args.racine, "videos_sources"), EXT_VIDEO)
    musiques = lister(os.path.join(args.racine, "musique"), EXT_AUDIO)
    if not sources:
        sys.exit(f"Aucune vidéo dans {os.path.join(args.racine, 'videos_sources')}")
    if not musiques:
        print("⚠ Aucune musique dans musique/ : vidéos générées sans son.")

    historique_chemin = os.path.join(args.racine, "historique.json")
    historique = []
    if os.path.exists(historique_chemin):
        with open(historique_chemin, encoding="utf-8") as f:
            historique = json.load(f)
    deja_vus = {tuple(h["blocs"]) for h in historique}

    jour = datetime.date.today().isoformat()
    with tempfile.TemporaryDirectory() as tmp:
        for compte in comptes:
            dossier = os.path.join(args.racine, "a_publier", jour, compte["nom"])
            os.makedirs(dossier, exist_ok=True)
            existantes = len(lister(dossier, EXT_VIDEO))
            messages_du_compte = {h["blocs"][1] for h in historique
                                  if h.get("compte") == compte["nom"] and len(h["blocs"]) > 1}
            for n in range(existantes + 1, compte["videos_par_jour"] + 1):
                video = ecrire_texte(compte, banque, deja_vus, messages_du_compte)
                source, debut = choisir_passage(sources, historique, args.duree)
                musique = random.choice(musiques) if musiques else None
                calque = os.path.join(tmp, f"calque_{compte['nom']}_{n}.png")
                rendre_calque(video["blocs"], calque)
                sortie = os.path.join(dossier, f"video_{n}.mp4")
                generer_video(source, debut, musique, calque, sortie, args.duree)
                with open(os.path.join(dossier, f"video_{n}_legende.txt"), "w", encoding="utf-8") as f:
                    f.write(video["legende"] + "\n")
                historique.append({
                    "date": jour,
                    "compte": compte["nom"],
                    "fichier": os.path.relpath(sortie, args.racine),
                    "source": os.path.basename(source),
                    "debut_source": round(debut, 2),
                    "musique": os.path.basename(musique) if musique else None,
                    "blocs": [b["texte"] for b in video["blocs"]],
                    "legende": video["legende"],
                })
                # Sauvegarde après chaque vidéo : rien n'est perdu si le PC s'éteint.
                with open(historique_chemin, "w", encoding="utf-8") as f:
                    json.dump(historique, f, ensure_ascii=False, indent=1)
                print(f"OK {compte['nom']}/video_{n}.mp4")

    print(f"Terminé : {os.path.join(args.racine, 'a_publier', jour)}")


if __name__ == "__main__":
    main()
