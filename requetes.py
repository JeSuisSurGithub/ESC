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

async def rqt_ajouter_compte(email, mdp, nom, prenom, date_naissance) -> typing.Tuple[bool, str]:
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
            "grade": 1})
        return (True, "Création du compte réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Création du compte échouée")

async def rqt_connexion_compte(email, mdp) -> typing.Tuple[bool, dict]:
    try:
        requete = "SELECT id, email, mdp, nom, prenom, date_naissance, grade FROM UTILISATEUR WHERE email=:email"
        resultats = await G_DB.fetch_all(requete, {"email": email})
        if len(resultats) == 0:
            raise ValueError("Aucun compte associé")

        hash_mdp_db = resultats[0]["mdp"]
        if not (bcrypt.checkpw(mdp.encode("utf-8"), hash_mdp_db)):
            raise ValueError("Mot de passe incorrect")

        resultat_dict = {
            "id": resultats[0]["id"],
            "email": resultats[0]["email"],
            "nom": resultats[0]["nom"],
            "prenom": resultats[0]["prenom"],
            "date_naissance": resultats[0]["date_naissance"],
            "grade": resultats[0]["grade"]}

        return (True, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return (False, {
            "id": "ERREUR",
            "email": "ERREUR",
            "nom": "ERREUR",
            "prenom": "ERREUR",
            "date_naissance": "ERREUR",
            "grade": "ERREUR"})

async def rqt_supprimer_compte(id) -> typing.Tuple[bool, str]:
    try:
        requete = "DELETE FROM UTILISATEUR WHERE id=:id"
        await G_DB.execute(requete, {"id": id})
        return (True, "Suppression du compte réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Suppression du compte échouée")

async def rqt_ajout_livre(titre, genre, date_parution, guid_nfc) -> typing.Tuple[bool, str]:
    try:
        requete = "INSERT INTO LIVRE (titre, genre, date_parution, guid_nfc) VALUES (:titre, :genre, :date_parution, :guid_nfc)"
        await G_DB.execute(requete, {"titre": titre, "genre": genre, "date_parution": date_parution, "guid_nfc": guid_nfc})
        return (True, "Ajout du livre réussi")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Ajout du livre échoué")

async def rqt_obtenir_livre() -> typing.Tuple[bool, dict]:
    try:
        requete = "SELECT id, titre, genre, date_parution, guid_nfc FROM LIVRE"
        resultats = await G_DB.fetch_all(requete)
        resultat_dict = {"id": [], "titre": [], "genre": [], "date_parution": [], "guid_nfc": []}
        for ligne in resultats:
            resultat_dict["id"].append(ligne["id"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
        return (True, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return(False, {"id": [-1], "titre": ["ERREUR"], "genre": ["ERREUR"], "date_parution": ["ERREUR"], "guid_nfc": ["ERREUR"]})

async def rqt_retirer_livre(id) -> typing.Tuple[bool, str]:
    try:
        requete = "DELETE FROM LIVRE WHERE id=:id"
        await G_DB.execute(requete, {"id": id})
        return (True, "Suppression du livre réussie")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Suppression du livre échouée")

async def rqt_emprunter(id_u, id_l, date_debut, date_fin) -> typing.Tuple[bool, str]:
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

async def rqt_obtenir_emprunts_u(id_u) -> typing.Tuple[bool, dict]:
    try:
        requete = '''
SELECT LIVRE.id as id_l, titre, genre, date_parution, guid_nfc, EMPRUNT.id as id_e, date_debut, date_fin, rendu
    FROM LIVRE JOIN EMPRUNT
    ON LIVRE.id==EMPRUNT.id_l WHERE id_u=:id_u'''
        resultats = await G_DB.fetch_all(requete, {"id_u": id_u})
        resultat_dict = {"id_livre": [], "titre": [], "genre": [], "date_parution": [], "guid_nfc": [], "id_emprunt": [],
            "debut_emprunts": [], "fin_emprunts": [], "rendu_emprunts": []}
        for ligne in resultats:
            resultat_dict["id_livre"].append(ligne["id_l"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
            resultat_dict["id_emprunt"].append(ligne["id_e"])
            resultat_dict["date_debut"].append(ligne["date_debut"])
            resultat_dict["date_fin"].append(ligne["date_fin"])
            resultat_dict["rendu"].append(ligne["rendu"])
        return (True, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return(False, {"id_livre": [-1], "titre": ["ERREUR"], "genre": ["ERREUR"], "date_parution": ["ERREUR"], "guid_nfc": ["ERREUR"],
        "id_emprunt": [-1], "date_debut": ["ERREUR"], "date_fin": ["ERREUR"], "rendu": ["ERREUR"]})

async def rqt_obtenir_emprunts_l(id_l) -> typing.Tuple[bool, dict]:
    try:
        requete = '''
SELECT LIVRE.id as id_l, titre, genre, date_parution, guid_nfc, EMPRUNT.id as id_e, date_debut, date_fin, rendu
    FROM LIVRE JOIN EMPRUNT
    ON LIVRE.id==EMPRUNT.id_l WHERE id_l=:id_l'''
        resultats = await G_DB.fetch_all(requete, {"id_l": id_l})
        resultat_dict = {"id_livre": [], "titre": [], "genre": [], "date_parution": [], "guid_nfc": [], "id_emprunt": [],
            "debut_emprunts": [], "fin_emprunts": [], "rendu_emprunts": []}
        for ligne in resultats:
            resultat_dict["id_livre"].append(ligne["id_l"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
            resultat_dict["id_emprunt"].append(ligne["id_e"])
            resultat_dict["date_debut"].append(ligne["date_debut"])
            resultat_dict["date_fin"].append(ligne["date_fin"])
            resultat_dict["rendu"].append(ligne["rendu"])
        return (True, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return(False, {"id_livre": [-1], "titre": ["ERREUR"], "genre": ["ERREUR"], "date_parution": ["ERREUR"], "guid_nfc": ["ERREUR"],
        "id_emprunt": [-1], "date_debut": ["ERREUR"], "date_fin": ["ERREUR"], "rendu": ["ERREUR"]})

async def rqt_retour(id):
    try:
        requete = "UPDATE EMPRUNT SET rendu=:rendu WHERE id=:id"
        await G_DB.execute(requete, {"rendu": True, "id": id})
        return (True, "Retour réussi")
    except Exception as e:
        print(f"Error: {e}")
        return (False, "Retour échoué")