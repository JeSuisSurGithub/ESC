# IMPORTE
# bcrypt pour le hachage des mot de passes
# databases pour des opérations sqlite thread-safe
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
# Lister emprunt par compte
# Lister emprunt par livre
# Rendre

import bcrypt
import databases

import erreurs

G_DB = databases.Database("sqlite:///./db/esc.sqlite")

async def rqt_connexion():
    await G_DB.connect()

async def rqt_deconnexion():
    await G_DB.disconnect()

async def rqt_ajouter_compte(email, mdp, pseudo, date_naissance):
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

async def rqt_connexion_compte(email, mdp):
    try:
        requete = "SELECT id, email, mdp, pseudo, date_naissance, grade FROM UTILISATEUR WHERE email=:email"
        resultats = await G_DB.fetch_all(requete, {"email": email})
        if len(resultats) == 0:
            raise ValueError("Aucun compte associé")

        hash_mdp_db = resultats[0]["mdp"]
        if not (bcrypt.checkpw(mdp.encode("utf-8"), hash_mdp_db)):
            raise ValueError("Mot de passe incorrect")

        json = {
            "id": resultats[0]["id"],
            "email": resultats[0]["email"],
            "pseudo": resultats[0]["pseudo"],
            "date_naissance": resultats[0]["date_naissance"],
            "grade": resultats[0]["grade"]}

        return (erreurs.OK_RQT_COMPTE_CONN, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_CONN, None)

async def rqt_supprimer_compte(id_u):
    try:
        requete = "DELETE FROM UTILISATEUR WHERE id=:id"
        await G_DB.execute(requete, {"id": id_u})
        return (erreurs.OK_RQT_COMPTE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_SUPP, None)

async def rqt_ajout_livre(titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image):
    try:
        requete = '''INSERT INTO LIVRE (titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image)
            VALUES (:titre, :genre, :auteur, :editeur, :rayon, :date_parution, :uid_nfc, :nom_image)'''
        await G_DB.execute(requete, {
            "titre": titre,
            "genre": genre,
            "auteur": auteur,
            "editeur": editeur,
            "rayon": rayon,
            "date_parution": date_parution,
            "uid_nfc": uid_nfc,
            "nom_image": nom_image})
        return (erreurs.OK_RQT_LIVRE_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_CREA, None)

async def rqt_obtenir_livre():
    try:
        requete = "SELECT id, titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image FROM LIVRE"
        resultats = await G_DB.fetch_all(requete)
        json = {
            "id": [],
            "titre": [],
            "genre": [],
            "auteur": [],
            "editeur": [],
            "rayon": [],
            "date_parution": [],
            "uid_nfc": [],
            "nom_image": []}

        for ligne in resultats:
            for cle in json.keys():
                json[cle].append(ligne[cle])

        return (erreurs.OK_RQT_LIVRE_LIST, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_LIST, None)

async def rqt_retirer_livre(id_l):
    try:
        requete = "DELETE FROM LIVRE WHERE id=:id"
        await G_DB.execute(requete, {"id": id_l})
        return (erreurs.OK_RQT_LIVRE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_SUPP, None)

async def rqt_emprunter(id_u, id_l, date_debut, date_fin):
    try:
        requete = '''INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
            VALUES (:id_u, :id_l, :date_debut, :date_fin, :rendu)'''
        await G_DB.execute(requete, {
            "id_u": id_u,
            "id_l": id_l,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "rendu": False})
        return (erreurs.OK_RQT_EMPRUNT_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_CREA, None)

async def rqt_obtenir_emprunts(id_u):
    try:
        requete = '''SELECT titre, genre, auteur, editeur, date_parution, nom_image,
            date_debut, date_fin, rendu
            FROM LIVRE JOIN EMPRUNT
                ON LIVRE.id==EMPRUNT.id_l WHERE id_u=:id_u'''
        resultats = await G_DB.fetch_all(requete, {"id_u": id_u})
        json = {
            "titre": [],
            "genre": [],
            "auteur": [],
            "editeur": [],
            "date_parution": [],
            "nom_image": [],
            "date_debut": [],
            "date_fin": [],
            "rendu": []}

        for ligne in resultats:
            for cle in json.keys():
                json[cle].append(ligne[cle])

        return (erreurs.OK_RQT_EMPRUNT_LIST, json)
    except Exception as e:
        print(f"Error: {e}")
        return(erreurs.ER_RQT_EMPRUNT_LIST, None)

async def rqt_obtenir_livre_par_uid(uid_nfc):
    try:
        requete = '''SELECT
            titre, genre, auteur, editeur, rayon, date_parution, nom_image, EMPRUNT.id as id_e, id_u, rendu,
            FROM LIVRE JOIN EMPRUNT
                ON LIVRE.id==EMPRUNT.id_l WHERE uid_nfc=:uid_nfc
                ORDER BY EMPRUNT.id DESC LIMIT 1'''
        resultats = await G_DB.fetch_all(requete, {"uid_nfc": uid_nfc})
        json = {
            "titre": None,
            "genre": None,
            "auteur": None,
            "editeur": None,
            "rayon": None,
            "date_parution": None,
            "nom_image": None,
            "id_e": None,
            "id_u": None,
            "rendu": None}

        if len(resultats) != 0:
            json = {
                "titre": resultats[0]["titre"],
                "genre": resultats[0]["genre"],
                "auteur": resultats[0]["auteur"],
                "editeur": resultats[0]["editeur"],
                "rayon": resultats[0]["rayon"],
                "date_parution": resultats[0]["date_parution"],
                "nom_image": resultats[0]["nom_image"],
                "id_e": resultats[0]["id_e"],
                "id_u": resultats[0]["id_u"],
                "rendu": resultats[0]["rendu"]}

        return (erreurs.OK_RQT_LIVRE_INFO_UID, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_INFO_UID, None)

async def rqt_retour(id_e):
    try:
        requete = "UPDATE EMPRUNT SET rendu=:rendu WHERE id=:id"
        await G_DB.execute(requete, {"rendu": True, "id": id_e})
        return (erreurs.OK_RQT_EMPRUNT_MOD_RETOUR, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_MOD_RETOUR, None)