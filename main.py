#!/bin/python3
# Script Serveur

from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from timeout_decorator import timeout
import uvicorn

import base64
from datetime import datetime, timedelta
import io
import os
from pathlib import Path

# https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
def est_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

DUREE_EMPRUNT_SEMAINE = 2

G_INFO_CONNEXION = None
G_CAPTEUR_EN_UTILISATION = False
G_EST_RASPBERRYPI = est_raspberrypi();

import erreurs
if G_EST_RASPBERRYPI:
    import nfc
import requetes

class JsonInscription(BaseModel):
    email: str
    motdepasse: str
    pseudo: str
    naissance: str

class JsonConnexion(BaseModel):
    email: str
    motdepasse: str

class JsonAjoutLivre(BaseModel):
    titre: str
    genre: str
    auteur: str
    editeur: str
    rayon: str
    date_parution: str
    uid_nfc: str
    nom_image: str
    image_b64: str

class JsonUidLivre(BaseModel):
    uid_nfc: str

class JsonRecherche(BaseModel):
    termes: list

@asynccontextmanager
async def lifespan(app: FastAPI):
    await requetes.rqt_connexion()
    yield
    await requetes.rqt_deconnexion()

Path("upload").mkdir(parents=True, exist_ok=True)

app = FastAPI(lifespan=lifespan)

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/html", StaticFiles(directory="html"), name="html")
app.mount("/img", StaticFiles(directory="img"), name="img")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")

@app.get("/")
def racine() -> str:
    return RedirectResponse(url="/html/connexion.html")

@app.get("/api_statut")
async def api_statut():
    global G_INFO_CONNEXION
    # Pas connecté
    if G_INFO_CONNEXION == None:
        return {"code": erreurs.ER_API_INFO_CONN}
    return {"code": erreurs.OK_API_INFO_CONN, "val": G_INFO_CONNEXION}

@app.get("/api_deconnexion")
async def api_deconnexion():
    global G_INFO_CONNEXION

    G_INFO_CONNEXION = None
    return {"code": erreurs.OK_API_DECONNECT}

@app.post("/api_inscription")
async def api_inscription(info_inscription: JsonInscription):
    global G_INFO_CONNEXION

    email = info_inscription.email
    motdepasse = info_inscription.motdepasse
    pseudo = info_inscription.pseudo
    naissance = info_inscription.naissance

    code, val = await requetes.rqt_ajout_compte(email, motdepasse, pseudo, naissance)
    # Déconnecte le compte auquel il est actuellement connecté
    if (code > 0):
        G_INFO_CONNEXION = None
    return {"code": code, "val": val}

@app.post("/api_connexion")
async def api_connexion(info_conn: JsonConnexion):
    global G_INFO_CONNEXION

    email = info_conn.email
    motdepasse = info_conn.motdepasse

    code, val = await requetes.rqt_connexion_compte(email, motdepasse)
    # Preuve de connexion
    if (code > 0):
        G_INFO_CONNEXION = val
    return {"code": code, "val": val}

@app.post("/api_desinscription")
async def api_desinscription(info_conn: JsonConnexion):
    global G_INFO_CONNEXION

    # Admin si grade = 0, Usager régulier si grade != 0
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        email = info_conn.email
        motdepasse = info_conn.motdepasse

        # Vérification identifiants
        code, val = await requetes.rqt_connexion_compte(email, motdepasse)
        if (code > 0):
            # Suppression et déconnexion
            code, val = await requetes.rqt_suppression_compte(val["id"])
            if (code > 0):
                G_INFO_CONNEXION = None
        return {"code": code, "val": val}
    else:
        return {"code": erreurs.ER_API_DROIT_USAGER}

@app.post("/api_ajout_livre")
async def api_ajout_livre(info_ajout: JsonAjoutLivre):
    global G_INFO_CONNEXION

    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] == 0):

        titre = info_ajout.titre
        genre = info_ajout.genre
        auteur = info_ajout.auteur
        editeur = info_ajout.editeur
        rayon = info_ajout.rayon
        date_parution = info_ajout.date_parution
        uid_nfc = info_ajout.uid_nfc
        nom_image = info_ajout.nom_image
        image_b64 = info_ajout.image_b64

        try:
            with open(f"upload/{nom_image}", "wb") as f:
                f.write(base64.b64decode(image_b64))
        except:
            return {"code": erreurs.ER_RQT_LIVRE_CREA}

        code, val = await requetes.rqt_ajout_livre(titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image)

        return {"code": code, "val": val}
    return {"code": erreurs.ER_API_DROIT_ADMIN}

@app.get("/api_info_livre")
async def api_info_livre(uid_nfc: str):
    code, val = await requetes.rqt_info_livre_par_uid(uid_nfc)
    return {"code": code, "val": val}

@app.post("/api_recherche_livre")
async def api_recherche_livre(info_recherche: JsonRecherche):
    termes = info_recherche.termes
    code, val = await requetes.rqt_info_livres_par_termes(termes)
    return {"code": code, "val": val}

@app.post("/api_suppression_livre")
async def api_suppression_livre(info_suppression: JsonUidLivre):
    global G_INFO_CONNEXION

    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] == 0):
        # Vérification de la disponibilité du livre
        code, val = await requetes.rqt_info_emprunt_par_uid(info_suppression.uid_nfc)
        if (code > 0):
            if (val["disponible"] != None) and (val["disponible"] == False):
                return {"code": erreurs.ER_API_EMPRUNT_ACTIF}

            # Obtention chemin d'image
            code, val = await requetes.rqt_livre_par_uid(uid_nfc)
            if (code > 0):
                nom_image = val['nom_image']

                # Suppression
                code, val = await requetes.rqt_retrait_livre(info_supp.uid_nfc)
                if (code > 0):
                    os.remove(f"upload/{nom_image}")

        return {"code": code, "val": val}
    return {"code": erreurs.ER_API_DROIT_ADMIN}

@app.post("/api_emprunt")
async def api_emprunt(info_emprunt: JsonUidLivre):
    global G_INFO_CONNEXION

    uid_nfc = info_emprunt.uid_nfc

    date_debut = datetime.now()
    date_fin = datetime.now() + timedelta(weeks=DUREE_EMPRUNT_SEMAINE)

    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        # Vérifie si il déja été emprunté
        code, val = await requetes.rqt_info_emprunt_par_uid(uid_nfc)
        if (code > 0):
            if (val["disponible"] != None) and (val["disponible"] == False):
                return {"code": erreurs.ER_API_EMPRUNT_ACTIF}

            # Obtention de l'ID Livre
            code, val = await requetes.rqt_livre_par_uid(uid_nfc)
            if (code > 0):
                code, val = await requetes.rqt_emprunt(G_INFO_CONNEXION["id"],  val["id"], date_debut.strftime("%Y-%m-%d"), date_fin.strftime("%Y-%m-%d"))
            return {"code": code, "val": val}
        else :
            return {"code": code}
    return {"code": erreurs.ER_API_DROIT_USAGER}

@app.get("/api_liste_emprunts")
async def api_liste_emprunts():
    global G_INFO_CONNEXION

    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        code, val = await requetes.rqt_liste_emprunts_par_compte(G_INFO_CONNEXION["id"])
        return {"code": code, "val": val}
    return {"code": erreurs.ER_API_DROIT_USAGER}

@app.get("/api_info_emprunt")
async def api_info_emprunt(uid_nfc: str):
    code, val = await requetes.rqt_info_emprunt_par_uid(uid_nfc)
    return {"code": code, "val": val}

@app.post("/api_retour")
async def api_retour(info_retour: JsonUidLivre):
    global G_INFO_CONNEXION

    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        uid_nfc = info_retour.uid_nfc

        # Vérification de si le livre a été emprunté
        code, val = await requetes.rqt_info_emprunt_par_uid(uid_nfc)
        if (code > 0):
            # Aucun emprunt
            if (val["disponible"] == None) or (val["disponible"] == True):
                return {"code": erreurs.ER_API_EMPRUNT_INACTIF}

            # Emprunté depuis un compte différent
            if (val["id_u"] != G_INFO_CONNEXION["id"]):
                return {"code": erreurs.ER_API_EMPRUNT_DROIT_COMPTE}

            code, val = await requetes.rqt_retour_emprunt(val["id_e"])

            return {"code": code, "val": val}
    return {"code": erreurs.ER_API_DROIT_USAGER}

@app.get("/api_uid_nfc")
async def api_uid_nfc():
    global G_CAPTEUR_EN_UTILISATION

    if (G_CAPTEUR_EN_UTILISATION):
        return {"code": erreurs.ER_API_CAPTEUR_OCCUPE}
    else:
        G_CAPTEUR_EN_UTILISATION = True
        @timeout(10)
        def timeout10():
            if (G_EST_RASPBERRYPI):
                return nfc.nfc_lire_uid()
            else:
                return (erreurs.OK_NFC_CAPTEUR_UID_MANUEL, input("Veuillez entrer l'UID: "))

        code, val = timeout10()
        G_CAPTEUR_EN_UTILISATION = False
        return {"code": code, "val": val}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")