#!/bin/python3

import asyncio
import bcrypt
import databases

import sys

G_DB = databases.Database("sqlite:///./esc.sqlite")

async def connexion_bd():
    await G_DB.connect()

async def deconnexion_bd():
    await G_DB.disconnect()

async def ajouter_compte(email, mdp, pseudo, date_naissance, grade):
    try:
        hash_mdp = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())
        requete = '''INSERT INTO UTILISATEUR (email, mdp, pseudo, date_naissance, grade)
            VALUES (:email, :mdp, :pseudo, :date_naissance, :grade)'''
        await G_DB.execute(requete, {
            "email": email,
            "mdp": hash_mdp,
            "pseudo": pseudo,
            "date_naissance": date_naissance,
            "grade": grade})
    except Exception as e:
        print(f"Error: {e}")

if len(sys.argv) != 6:
    print(f"Utilisation: {sys.argv[0]} exemple@email.com motdepasse pseudo AAAA-MM-JJ (date de naissance) GRADE")
    exit(1)

email           = sys.argv[1]
mdp             = sys.argv[2]
pseudo          = sys.argv[3]
date_naissance  = sys.argv[4]
grade           = sys.argv[5]

asyncio.run(connexion_bd())
asyncio.run(ajouter_compte(email, mdp, pseudo, date_naissance, grade))
asyncio.run(deconnexion_bd())

exit(0)