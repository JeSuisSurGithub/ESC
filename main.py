#!/bin/python3

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

import requetes

class JSONInscription(BaseModel):
    email: str
    motdepasse: str
    nom: str
    prenom: str
    naissance: str

class JSONConnexion(BaseModel):
    email: str
    motdepasse: str

class JSONEmprunts(BaseModel):
    id_u: str

app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/html", StaticFiles(directory="html"), name="html")

class InfoConnexion:
    def __init__(self, id, email, nom, prenom, date_naissance, grade):
        self.id = id
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.grade = grade

def conv_class_dict(infoconn):
    return {
        "id": infoconn.id,
        "email": infoconn.email,
        "nom": infoconn.nom,
        "prenom": infoconn.prenom,
        "date_naissance": infoconn.date_naissance,
        "grade": infoconn.grade}

G_INFO_CONNEXION = None

@app.on_event("startup")
async def startup_db():
    await requetes.rqt_connexion()

@app.on_event("shutdown")
async def shutdown_db():
    await requetes.rqt_deconnexion()

@app.get("/")
def racine() -> str:
    return FileResponse('html/index.html')

@app.get("/sql_statut")
async def sql_statut():
    if G_INFO_CONNEXION == None:
        return {"resultat": False}
    return {"resultat": True, "donnees": conv_class_dict(G_INFO_CONNEXION)}

@app.post("/sql_deconnexion")
async def sql_deconnexion():
    global G_INFO_CONNEXION
    G_INFO_CONNEXION = None
    return {"resultat": True}

@app.post("/sql_inscription")
async def sql_inscription(user: JSONInscription):
    email = user.email
    motdepasse = user.motdepasse
    nom = user.nom
    prenom = user.prenom
    naissance = user.naissance
    res, msg = await requetes.rqt_ajouter_compte(email, motdepasse, nom, prenom, naissance)
    return {"resultat": res, "donnees": msg}

@app.post("/sql_connexion")
async def sql_connexion(user: JSONConnexion):
    global G_INFO_CONNEXION
    email = user.email
    motdepasse = user.motdepasse
    res, info = await requetes.rqt_connexion_compte(email, motdepasse)
    G_INFO_CONNEXION = InfoConnexion(info["id"], info["email"], info["nom"], info["prenom"], info["date_naissance"], info["grade"])
    return {"resultat": res, "donnees": conv_class_dict(G_INFO_CONNEXION)}

@app.post("/sql_desinscription")
async def sql_desinscription(user: JSONConnexion):
    global G_INFO_CONNEXION
    email = user.email
    motdepasse = user.motdepasse
    res, msg = await requetes.rqt_connexion_compte(email, motdepasse)
    if (res):
        res, msg = await requetes.rqt_supprimer_compte(G_INFO_CONNEXION.id)
    G_INFO_CONNEXION = None
    return {"resultat": res, "donnees": msg}

@app.get("/sql_livres")
async def sql_livres():
    res, donnees = await requetes.rqt_obtenir_livre()
    return {"resultat": res, "donnees": donnees}

@app.get("/sql_livres_empruntes")
async def sql_livres_empruntes(info_emprunts: JSONEmprunts):
    res, donnees = await requetes.rqt_obtenir_emprunts(info_emprunts.id_u)
    return {"resultat": res, "donnees": donnees}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')