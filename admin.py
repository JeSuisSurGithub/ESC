#!/bin/python3
import databases
import bcrypt
import asyncio
import typing
import sys

G_DB = databases.Database("sqlite:///./esc.db")

async def connexion_bd():
    await G_DB.connect()

async def deconnexion_bd():
    await G_DB.disconnect()

async def ajouter_compte(email, mdp, nom, prenom, date_naissance, grade) -> typing.Tuple[bool, str]:
    try:
        hash_mdp = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())
        requete = '''INSERT INTO UTILISATEUR (email, mdp, nom, prenom, date_naissance, grade)
            VALUES (:email, :mdp, :nom, :prenom, :date_naissance, :grade)'''
        await G_DB.execute(requete, {
            "email": email,
            "mdp": hash_mdp,
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "grade": grade})
        return (True, "Création du compte réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Création du compte échouée")

if len(sys.argv) != 6:
    print(f"Utilisation: {sys.argv[0]} exemple@email.com motdepasse nom prenom AAAA-MM-JJ (date de naissance) GRADE")
    exit(1)

email           = sys.argv[1]
mdp             = sys.argv[2]
nom             = sys.argv[3]
prenom          = sys.argv[4]
date_naissance  = sys.argv[5]
grade           = sys.argv[6]

asyncio.run(connexion_bd())
asyncio.run(ajouter_compte(email, mdp, nom, prenom, date_naissance, grade))
asyncio.run(deconnexion_bd())

exit(0)