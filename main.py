#!/bin/python3

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from timeout_decorator import timeout
import time

import requetes
import nfc

G_INFO_CONNEXION = None
G_CAPTEUR_EN_UTILISATION = False

class JSONInscription(BaseModel):
    email: str
    motdepasse: str
    pseudo: str
    naissance: str

class JSONConnexion(BaseModel):
    email: str
    motdepasse: str

class JSONAjoutLivre(BaseModel):
    titre: str
    genre: str
    rayon: str
    date_parution: str
    guid_nfc: str

class JSONIDLivre(BaseModel):
    id_l: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await requetes.rqt_connexion()
    yield
    await requetes.rqt_deconnexion()

app = FastAPI(lifespan=lifespan)

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/html", StaticFiles(directory="html"), name="html")
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/")
def racine() -> str:
    return FileResponse('html/index.html')

@app.get("/api_statut")
async def api_statut():
    if G_INFO_CONNEXION == None:
        return {"resultat": False, "donnees": "Vous n'êtes pas connecté"}
    return {"resultat": True, "donnees": G_INFO_CONNEXION}

@app.post("/api_deconnexion")
async def api_deconnexion():
    global G_INFO_CONNEXION
    G_INFO_CONNEXION = None
    return {"resultat": True, "donnees": "Déconnecté"}

@app.post("/api_inscription")
async def api_inscription(info_reg: JSONInscription):
    email = info_reg.email
    motdepasse = info_reg.motdepasse
    pseudo = info_reg.pseudo
    naissance = info_reg.naissance
    res, msg = await requetes.rqt_ajouter_compte(email, motdepasse, pseudo, naissance)
    if (res):
        # On déconnecte le compte au cas ou il est actuellement connecté à un compte
        G_INFO_CONNEXION = None
    return {"resultat": res, "donnees": msg}

@app.post("/api_connexion")
async def api_connexion(info_conn: JSONConnexion):
    global G_INFO_CONNEXION
    email = info_conn.email
    motdepasse = info_conn.motdepasse
    res, info = await requetes.rqt_connexion_compte(email, motdepasse)
    if (res):
        G_INFO_CONNEXION = info
    return {"resultat": res, "donnees": info}

@app.post("/api_desinscription")
async def api_desinscription(info_conn: JSONConnexion):
    global G_INFO_CONNEXION
    email = info_conn.email
    motdepasse = info_conn.motdepasse
    res, msg = await requetes.rqt_connexion_compte(email, motdepasse)
    if (res):
        res, msg = await requetes.rqt_supprimer_compte(G_INFO_CONNEXION["id"])
        if (res):
            G_INFO_CONNEXION = None
    return {"resultat": res, "donnees": msg}

@app.post("/api_ajout")
async def api_ajout(info_ajout: JSONAjoutLivre):
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] == 0):
        titre = info_ajout.titre
        genre = info_ajout.genre
        rayon = info_ajout.rayon
        date_parution = info_ajout.date_parution
        guid_nfc = info_ajout.guid_nfc
        res, msg = await requetes.rqt_ajout_livre(titre, genre, rayon, date_parution, guid_nfc)
        return {"resultat": res, "donnees": msg}
    return {"resultat": False, "donnees": "Vous n'êtes pas administrateur"}

@app.get("/api_livres")
async def api_livres():
    res, info = await requetes.rqt_obtenir_livre()
    return {"resultat": res, "donnees": info}

@app.post("/api_retrait")
async def api_retrait(info_supp: JSONIDLivre):
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] == 0):
        res, msg = await requetes.rqt_retirer_livre(info_supp.id_l)
        return {"resultat": res, "donnees": msg}
    return {"resultat": False, "donnees": "Vous n'êtes pas administrateur"}

@app.post("/api_emprunt")
async def api_emprunt(info_emprunt: JSONIDLivre):
    id_l = info_emprunt.id_l
    date_debut = datetime.now()
    date_fin = datetime.now() + timedelta(weeks=2)
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        res, info = await requetes.rqt_obtenir_emprunts_l(id_l)
        if (len(info) != 0 and info[-1]["rendu"] == False):
            return {"resultat": False, "donnees": "Livre déja emprunté"}
        else:
            res, msg = await requetes.rqt_emprunter(G_INFO_CONNEXION["id"], id_l, date_debut.strftime("%Y-%m-%d"), date_fin.strftime("%Y-%m-%d"))
            return {"resultat": res, "donnees": msg}
    return {"resultat": False, "donnees": "Vous n'êtes pas un usager"}

@app.get("/api_emprunt_livres")
async def api_emprunt_livres():
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        res, info = await requetes.rqt_obtenir_emprunts_u(G_INFO_CONNEXION["id"])
        return {"resultat": res, "donnees": info}
    return {"resultat": False, "donnees": "Vous n'êtes pas un usager"}

@app.get("/api_hist_livre")
async def api_hist_livre(id_l: str):
    res, info = await requetes.rqt_obtenir_emprunts_l(id_l)
    return {"resultat": res, "donnees": info}

@app.post("/api_retour")
async def api_retour(info_retour: JSONIDLivre):
    if (G_INFO_CONNEXION != None) and (G_INFO_CONNEXION["grade"] != 0):
        id_l = info_retour.id_l
        res, info = await requetes.rqt_obtenir_emprunts_l(id_l)
        if (len(info) == 0):
            return {"resultat": False, "donnees": "Livre jamais emprunté"}
        elif (info[-1]["rendu"] == True):
            return {"resultat": False, "donnees": "Livre déja rendu"}
        else:
            res, msg = await requetes.rqt_retour(info[-1]["id_emprunt"])
            return {"resultat": res, "donnees": msg}
    return {"resultat": False, "donnees": "Vous n'êtes pas un usager"}

@app.get("/api_uid_nfc")
async def api_uid_nfc():
    global G_CAPTEUR_EN_UTILISATION
    if (G_CAPTEUR_EN_UTILISATION):
        return {"resultat": false, "donnees": "Capteur en cours d'utilisation"}
    else:
        G_CAPTEUR_EN_UTILISATION = True
        @timeout(10)
        def timeout10():
            return nfc.lire_uid_nfc()

        res, donnees = timeout10()
        G_CAPTEUR_EN_UTILISATION = False
        return {"resultat": res, "donnees": donnees}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')