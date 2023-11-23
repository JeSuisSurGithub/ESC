#!/bin/python3

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

class JSONInscription(BaseModel):
    email: str
    motdepasse: str
    nom: str
    prenom: str
    naissance: str

class JSONConnexion(BaseModel):
    email: str
    motdepasse: str

class JSONLivres(BaseModel):
    titres: list[str]
    genres: list[str]
    date_parution: list[str]

class JSONEmprunts(BaseModel):
    titres: list[str]
    genres: list[str]
    date_parution: list[str]
    date_emprunt_debut: list[str]
    date_emprunt_fin: list[str]

app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/html", StaticFiles(directory="html"), name="html")

EST_CONNECTE = False

@app.get("/")
def racine() -> str:
    return FileResponse('html/index.html')

@app.get("/sql_statut")
async def sql_statut():
    return {"resultat": EST_CONNECTE, "grade": 0}

@app.post("/sql_deconnexion")
async def sql_deconnexion():
    global EST_CONNECTE
    EST_CONNECTE = False
    return {"resultat": True}

@app.post("/sql_inscription")
async def sql_inscription(user: JSONInscription):
    global EST_CONNECTE
    email = user.email
    motdepasse = user.motdepasse
    nom = user.nom
    prenom = user.prenom
    naissance = user.naissance
    print(email, motdepasse, nom, prenom, naissance)
    EST_CONNECTE = True
    return {"resultat": True}

@app.post("/sql_connexion")
async def sql_connexion(user: JSONConnexion):
    global EST_CONNECTE
    email = user.email
    motdepasse = user.motdepasse
    print(email, motdepasse)
    EST_CONNECTE = True
    return {"resultat": True}

@app.post("/sql_desinscription")
async def sql_desinscription(user: JSONConnexion):
    global EST_CONNECTE
    email = user.email
    motdepasse = user.motdepasse
    print(email, motdepasse)
    EST_CONNECTE = False
    return {"resultat": True}

@app.get("/sql_livres")
async def sql_statut():
    return {"titres": ["bible", "coran"], "genres": ["religion", "religion"], "date_parution": ["????", "????"]}

@app.get("/sql_livres_empruntes")
async def sql_statut():
    return {"titres": ["bible", "coran"], "genres": ["religion", "religion"], "date_parution": ["????", "????"], \
"date_emprunt_debut": ["2023-06-11", "2023-08-11"], "date_emprunt_fin": ["2023-06-25", "2023-08-25"]}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')