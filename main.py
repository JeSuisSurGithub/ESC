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

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')