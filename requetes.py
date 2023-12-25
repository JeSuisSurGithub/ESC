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

import erreurs

G_DB = databases.Database("sqlite:///./db/esc.db")

async def rqt_connexion():
    await G_DB.connect()

async def rqt_deconnexion():
    await G_DB.disconnect()

async def rqt_ajouter_compte(email, mdp, pseudo, date_naissance) -> typing.Tuple[bool, str]:
    try:
        hash_mdp = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())
        requete = '''INSERT INTO UTILISATEUR (email, mdp, pseudo, date_naissance, grade)
            VALUES (:email, :mdp, :pseudo, :date_naissance, :grade)'''
        await G_DB.execute(requete, {
            "email": email,
            "mdp": hash_mdp,
            "pseudo": pseudo,
            "date_naissance": date_naissance,
            "grade": 1})
        return (erreurs.OK_RQT_COMPTE_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_CREA, None)

async def rqt_connexion_compte(email, mdp) -> typing.Tuple[bool, dict]:
    try:
        requete = "SELECT id, email, mdp, pseudo, date_naissance, grade FROM UTILISATEUR WHERE email=:email"
        resultats = await G_DB.fetch_all(requete, {"email": email})
        if len(resultats) == 0:
            raise ValueError("Aucun compte associé")

        hash_mdp_db = resultats[0]["mdp"]
        if not (bcrypt.checkpw(mdp.encode("utf-8"), hash_mdp_db)):
            raise ValueError("Mot de passe incorrect")

        resultat_dict = {
            "id": resultats[0]["id"],
            "email": resultats[0]["email"],
            "pseudo": resultats[0]["pseudo"],
            "date_naissance": resultats[0]["date_naissance"],
            "grade": resultats[0]["grade"]}

        return (erreurs.OK_RQT_COMPTE_CONN, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_CONN, None)

async def rqt_supprimer_compte(id_u) -> typing.Tuple[bool, str]:
    try:
        requete = "DELETE FROM UTILISATEUR WHERE id=:id"
        await G_DB.execute(requete, {"id": id_u})
        return (erreurs.OK_RQT_COMPTE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_SUPP, None)

async def rqt_ajout_livre(titre, genre, rayon, date_parution, guid_nfc) -> typing.Tuple[bool, str]:
    try:
        requete = "INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc) VALUES (:titre, :genre, :date_parution, :guid_nfc)"
        await G_DB.execute(requete, {"titre": titre, "genre": genre, "rayon": rayon, "date_parution": date_parution, "guid_nfc": guid_nfc})
        return (erreurs.OK_RQT_LIVRE_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_CREA, None)

async def rqt_obtenir_livre() -> typing.Tuple[bool, dict]:
    try:
        requete = "SELECT id, titre, genre, rayon, date_parution, guid_nfc FROM LIVRE"
        resultats = await G_DB.fetch_all(requete)
        resultat_dict = {"id": [], "titre": [], "genre": [], "rayon": [], "date_parution": [], "guid_nfc": []}
        for ligne in resultats:
            resultat_dict["id"].append(ligne["id"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["rayon"].append(ligne["rayon"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
        return (erreurs.OK_RQT_LIVRE_LIST, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_LIST, None)

async def rqt_retirer_livre(id_l) -> typing.Tuple[bool, str]:
    try:
        requete = "DELETE FROM LIVRE WHERE id=:id"
        await G_DB.execute(requete, {"id": id_l})
        return (erreurs.OK_RQT_LIVRE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_SUPP, None)

async def rqt_emprunter(id_u, id_l, date_debut, date_fin) -> typing.Tuple[bool, str]:
    try:
        requete = "INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu) VALUES (:id_u, :id_l, :date_debut, :date_fin, :rendu)"
        await G_DB.execute(requete,
            {"id_u": id_u, "id_l": id_l,
             "date_debut": date_debut, "date_fin": date_fin,
             "rendu": False})
        return (erreurs.OK_RQT_EMPRUNT_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_CREA, None)

async def rqt_obtenir_emprunts_u(id_u) -> typing.Tuple[bool, dict]:
    try:
        requete = '''
SELECT LIVRE.id as id_l, titre, genre, rayon, date_parution, guid_nfc, EMPRUNT.id as id_e, id_u, date_debut, date_fin, rendu
    FROM LIVRE JOIN EMPRUNT
    ON LIVRE.id==EMPRUNT.id_l WHERE id_u=:id_u'''
        resultats = await G_DB.fetch_all(requete, {"id_u": id_u})
        resultat_dict = {"id_livre": [], "titre": [], "genre": [], "rayon": [], "date_parution": [],
            "guid_nfc": [], "id_emprunt": [],
            "id_utilisateur": [], "date_debut": [], "date_fin": [], "rendu": []}
        for ligne in resultats:
            resultat_dict["id_l"].append(ligne["id_l"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["rayon"].append(ligne["rayon"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
            resultat_dict["id_e"].append(ligne["id_e"])
            resultat_dict["id_u"].append(ligne["id_u"])
            resultat_dict["date_debut"].append(ligne["date_debut"])
            resultat_dict["date_fin"].append(ligne["date_fin"])
            resultat_dict["rendu"].append(ligne["rendu"])
        return (erreurs.OK_RQT_EMPRUNT_LIST_COMPTE, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return(erreurs.ER_RQT_EMPRUNT_LIST_COMPTE, None)

async def rqt_obtenir_emprunts_l(id_l) -> typing.Tuple[bool, dict]:
    try:
        requete = '''
SELECT LIVRE.id as id_l, titre, genre, rayon, date_parution, guid_nfc, EMPRUNT.id as id_e, id_u, date_debut, date_fin, rendu
    FROM LIVRE JOIN EMPRUNT
    ON LIVRE.id==EMPRUNT.id_l WHERE id_l=:id_l'''
        resultats = await G_DB.fetch_all(requete, {"id_l": id_l})
        resultat_dict = {"id_livre": [], "titre": [], "genre": [], "rayon": [], "date_parution": [],
        "guid_nfc": [], "id_emprunt": [],
            "id_utilisateur": [], "date_debut": [], "date_fin": [], "rendu": []}
        for ligne in resultats:
            resultat_dict["id_l"].append(ligne["id_l"])
            resultat_dict["titre"].append(ligne["titre"])
            resultat_dict["genre"].append(ligne["genre"])
            resultat_dict["rayon"].append(ligne["rayon"])
            resultat_dict["date_parution"].append(ligne["date_parution"])
            resultat_dict["guid_nfc"].append(ligne["guid_nfc"])
            resultat_dict["id_e"].append(ligne["id_e"])
            resultat_dict["id_u"].append(ligne["id_u"])
            resultat_dict["date_debut"].append(ligne["date_debut"])
            resultat_dict["date_fin"].append(ligne["date_fin"])
            resultat_dict["rendu"].append(ligne["rendu"])
        return (erreurs.OK_RQT_EMPRUNT_LIST_LIVRE, resultat_dict)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_LIST_LIVRE, None)

async def rqt_retour(id_e):
    try:
        requete = "UPDATE EMPRUNT SET rendu=:rendu WHERE id=:id"
        await G_DB.execute(requete, {"rendu": True, "id": id_e})
        return (erreurs.OK_RQT_EMPRUNT_MOD_RETOUR, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_MOD_RETOUR, None)