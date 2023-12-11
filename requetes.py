#!/bin/python3

# IMPORTE
# databases pour des opérations sqlite asynchrones
# bcrypt pour le hachage des mot de passes
# typing pour le retour
#
# PLAN DES DEFINITIONS
#
# VARIABLE GLOBALE:
# G_DB objet de connexion
#
# FONCTIONS:
# Connexion à la BDD
# Déconnesion de la BDD
#
# Ajout compte
# Vérification connexion au compte
# Suppression compte
#
# Ajout livre
# Lister livre
# Suppression livre
#
# Emprunter
# Lister emprunt
# Rendre

import databases
import bcrypt
import typing

G_DB = databases.Database("sqlite:///./esc.db")

async def rqt_connexion():
    await G_DB.connect()

async def rqt_deconnexion():
    await G_DB.disconnect()

async def rqt_ajouter_compte(email, mdp, nom, prenom, date_naissance) -> Tuple[bool, str]:
    try:
        hash_mdp = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())
        requete = '''INSERT INTO UTILISATEUR (email, mdp, nom, prenom, date_naissance, grade)
            VALUES (:email, :mdp, :nom, :prenom, :date_naissance, :grade)'''
        await G_DB.execute(requete, {
            "email": email,
            "mdp": hash_mdp,
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "grade": 1})
        return (True, "Création du compte réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Création du compte échouée")

async def rqt_connexion_compte(email, mdp) -> Tuple[bool, str]:
    try:
        requete = "SELECT id, email, mdp, nom, prenom, date_naissance, grade FROM UTILISATEUR WHERE email=:email"
        resultats = await G_DB.fetch_all(requete, {"email": email})
        if len(resultats) == 0:
            raise ValueError("Aucun compte associé")

        hash_mdp_db = resultats[0]["mdp"]
        if not (bcrypt.checkpw(mdp.encode('utf-8'), hash_mdp_db.encode('utf-8'))):
            raise ValueError("Mot de passe incorrect")
        return (True, "Connexion réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Connexion échouée")

async def rqt_supprimer_compte(id) -> Tuple[bool, str]:
    try:
        requete = "DELETE FROM UTILISATEUR WHERE id=:id"
        await G_DB.execute(requete, {"id": id})
        return (True, "Suppression du compte réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Suppression du compte échouée")

async def rqt_ajout_livre(id, titre, genre, date_parution):
    try:
        requete = "INSERT INTO LIVRE (titre, genre, date_parution) VALUES (:titre, :genre, :date_parution)"
        await G_DB.execute(requete, {"titre": titre, "genre": genre, "date_parution": date_parution})
        return (True, "Ajout du livre réussi")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Ajout du livre échoué")

async def rqt_obtenir_livre() -> Tuple[bool, dict]:
    try:
        requete = "SELECT id, titre, genre, date_parution FROM LIVRE"
        resultats = await G_DB.fetch_all(requete)
        resultat_dict = {"ids": [], "titres": [], "genres": [], "dates": []}
        for ligne in resultats:
            resultat_dict["ids"].append(ligne["id"])
            resultat_dict["titres"].append(ligne["titre"])
            resultat_dict["genres"].append(ligne["genre"])
            resultat_dict["dates"].append(ligne["date_parution"])
        return (True, resultat_dict)
    except:
        return(True, {"ids": [-1], "titres": ["ERREUR"], "genres": ["ERREUR"], "dates": ["ERREUR"]})

async def rqt_retirer_livre(id) -> Tuple[bool, str]:
    try:
        requete = "DELETE FROM LIVRE WHERE id=:id"
        await G_DB.execute(requete, {"id": id})
        return (True, "Suppression du livre réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Suppression du livre échouée")

async def rqt_emprunter(id_u, id_l, date_debut, date_fin):
    try:
        requete = "INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu) VALUES (:id_u, :id_l, :date_debut, :date_fin, :rendu)"
        await G_DB.execute(requete,
            {"id_u": id_u, "id_l": id_l,
             "date_debut": date_debut, "date_fin": date_fin,
             "rendu": False})
        return (True, "Emprunt réussi")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Emprunt échoué")

async def rqt_obtenir_emprunts(id_u) -> Tuple[bool, dict]:
    try:
        requete = '''
SELECT LIVRE.id as id_l, titre, genre, date_parution, EMPRUNT.id as id_e, date_debut, date_fin, rendu
    FROM LIVRE JOIN EMPRUNT
    ON LIVRE.id==EMPRUNT.id_l WHERE id_u=:id_u'''
        resultats = await G_DB.fetch_all(requete, {"id_u": id_u})
        resultat_dict = {"id_livres": [], "titres": [], "genres": [], "dates": [], "id_emprunts": [],
            "debut_emprunts": [], "fin_emprunts": [], "rendu_emprunts": []}
        for ligne in resultats:
            resultat_dict["id_livres"].append(ligne["id_l"])
            resultat_dict["titres"].append(ligne["titre"])
            resultat_dict["genres"].append(ligne["genre"])
            resultat_dict["dates"].append(ligne["date_parution"])
            resultat_dict["id_emprunts"].append(ligne["id_e"])
            resultat_dict["debut_emprunts"].append(ligne["date_debut"])
            resultat_dict["fin_emprunts"].append(ligne["date_fin"])
            resultat_dict["rendu_emprunts"].append(ligne["rendu"])
        return (True, resultat_dict)
    except:
        return(True, {"id_livres": [-1], "titres": ["ERREUR"], "genres": ["ERREUR"], "dates": ["ERREUR"],
        "id_emprunts": [-1], "debut_emprunts": ["ERREUR"], "fin_emprunts": ["ERREUR"], "rendu_emprunts": ["ERREUR"]})

async def rqt_retour(id):
    try:
        requete = "UPDATE EMPRUNT SET rendu=:rendu WHERE id=:id"
        await G_DB.execute(requete, {"rendu": True, "id": id})
        return (True, "Retour réussi")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Retour échoué")