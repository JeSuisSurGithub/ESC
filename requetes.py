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
# Déconnexion de la BDD
#
# Ajout compte
# Vérification connexion au compte
# Suppression compte
#
# Ajout livre
# Info livre par UID
# Recherche livre
# Suppression livre
#
# Emprunter
# Info emprunt par UID
# Rendre

import bcrypt
import databases

import erreurs

G_DB = databases.Database("sqlite:///./db/esc.sqlite")

async def rqt_connexion():
    await G_DB.connect()

async def rqt_deconnexion():
    await G_DB.disconnect()

async def rqt_ajout_compte(email, mdp, pseudo, date_naissance):
    try:
        hash_mdp = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())

        requete = '''INSERT
            INTO UTILISATEUR (email, hash_mdp, pseudo, date_naissance, grade)
            VALUES (:email, :hash_mdp, :pseudo, :date_naissance, :grade)'''

        await G_DB.execute(requete, {
            "email": email,
            "hash_mdp": hash_mdp,
            "pseudo": pseudo,
            "date_naissance": date_naissance,
            "grade": 1})

        return (erreurs.OK_RQT_COMPTE_CREA, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_CREA, None)

async def rqt_connexion_compte(email, mdp):
    try:
        requete = '''SELECT
            id, email, hash_mdp, pseudo, date_naissance, grade
            FROM UTILISATEUR WHERE email=:email'''

        resultats = await G_DB.fetch_all(requete, {"email": email})

        if len(resultats) == 0:
            raise ValueError("Aucun compte associé")

        hash_mdp_db = resultats[0]["hash_mdp"]
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

async def rqt_suppression_compte(id_u):
    try:
        requete = "DELETE FROM UTILISATEUR WHERE id=:id"
        await G_DB.execute(requete, {"id": id_u})
        return (erreurs.OK_RQT_COMPTE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_COMPTE_SUPP, None)

async def rqt_ajout_livre(titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image):
    try:
        requete = '''INSERT
            INTO LIVRE (titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image)
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

async def rqt_info_livre_par_uid(uid_nfc):
    try:
        requete = '''SELECT
            id, titre, genre, auteur, editeur, rayon, date_parution, nom_image,
            FROM LIVRE uid_nfc=:uid_nfc
            ORDER BY EMPRUNT.id DESC LIMIT 1'''

        resultats = await G_DB.fetch_all(requete, {"uid_nfc": uid_nfc})

        json = {
            "id": None,
            "titre": None,
            "genre": None,
            "auteur": None,
            "editeur": None,
            "rayon": None,
            "date_parution": None,
            "nom_image": None,
        }

        if len(resultats) != 0:
            for cle in json.keys():
                json[cle] = resultats[0][cle]

        return (erreurs.OK_RQT_LIVRE_INFO_UID, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_INFO_UID, None)

async def rqt_info_livres_par_termes(termes):
    try:
        part_select = '''SELECT
            titre, genre, auteur, editeur, rayon, date_parution, nom_image
            FROM LIVRE'''

        # Recherche par titre, genre et auteur
        part_recherche = " OR ".join([f"(titre LIKE :terme_{i} OR genre LIKE :terme_{i} OR auteur LIKE :terme_{i})" for i in range(len(termes))])
        requete = f"{part_select} WHERE {part_recherche}"

        param = {}
        for i in range(len(termes)):
            param[f"terme_{i}"] = f"'%{termes[i]}%'"

        resultats = await G_DB.fetch_all(requete, param)

        json = {
            "titre": [],
            "genre": [],
            "auteur": [],
            "editeur": [],
            "rayon": [],
            "date_parution": [],
            "nom_image": []}

        for ligne in resultats:
            for cle in json.keys():
                json[cle].append(ligne[cle])

        return (erreurs.OK_RQT_LIVRE_RECHERCHE, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_RECHERCHE, None)

async def rqt_suppression_livre(uid_nfc):
    try:
        requete = "DELETE FROM LIVRE WHERE uid_nfc=:uid_nfc"
        await G_DB.execute(requete, {"uid_nfc": uid_nfc})
        return (erreurs.OK_RQT_LIVRE_SUPP, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_SUPP, None)

async def rqt_ajout_emprunt(id_u, id_l, date_debut, date_fin):
    try:
        requete = '''INSERT
            INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
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

async def rqt_liste_emprunts_par_compte(id_u):
    try:
        requete = '''SELECT
            titre, genre, auteur, editeur, date_parution, nom_image, date_debut, date_fin, rendu
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

async def rqt_info_emprunt_par_uid(uid_nfc):
    try:
        requete = '''SELECT
            rendu as disponible, id_u, EMPRUNT.id as id_e
            FROM LIVRE JOIN EMPRUNT
            ON LIVRE.id==EMPRUNT.id_l WHERE uid_nfc=:uid_nfc
            ORDER BY EMPRUNT.id DESC LIMIT 1'''

        resultats = await G_DB.fetch_all(requete, {"uid_nfc": uid_nfc})

        json = {"disponible": None, "id_u": None, "id_e": None}

        if len(resultats) != 0:
            json["disponible"] = resultats[0]["disponible"]
            json["id_u"] = resultats[0]["id_u"]
            json["id_e"] = resultats[0]["id_e"]

        return (erreurs.OK_RQT_LIVRE_DISPO, json)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_LIVRE_DISPO, None)

async def rqt_retour_emprunt(id_e):
    try:
        requete = "UPDATE EMPRUNT SET rendu=:rendu WHERE id=:id"
        await G_DB.execute(requete, {"rendu": True, "id": id_e})
        return (erreurs.OK_RQT_EMPRUNT_MOD_RETOUR, None)
    except Exception as e:
        print(f"Error: {e}")
        return (erreurs.ER_RQT_EMPRUNT_MOD_RETOUR, None)