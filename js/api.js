// -------------------- CODE ERREURS -------------------- //
const ER_INCONNU = 0;
const OK_RQT_COMPTE_CREA = 1;
const ER_RQT_COMPTE_CREA = -1;
const OK_RQT_COMPTE_CONN = 2;
const ER_RQT_COMPTE_CONN = -2;
const OK_RQT_COMPTE_SUPP = 3;
const ER_RQT_COMPTE_SUPP = -3;
const OK_RQT_LIVRE_CREA = 4;
const ER_RQT_LIVRE_CREA = -4;
const OK_RQT_LIVRE_LIST = 5;
const ER_RQT_LIVRE_LIST = -5;
const OK_RQT_LIVRE_SUPP = 6;
const ER_RQT_LIVRE_SUPP = -6;
const OK_RQT_EMPRUNT_CREA = 7;
const ER_RQT_EMPRUNT_CREA = -7;
const OK_RQT_EMPRUNT_LIST = 8;
const ER_RQT_EMPRUNT_LIST = -8;
const OK_RQT_LIVRE_INFO_UID = 9;
const ER_RQT_LIVRE_INFO_UID = -9;
const OK_RQT_EMPRUNT_MOD_RETOUR = 10;
const ER_RQT_EMPRUNT_MOD_RETOUR = -10;

const OK_API_INFO_CONN = 11;
const ER_API_INFO_CONN = -11;
const OK_API_DECONNECT = 12;
const ER_API_DROIT_ADMIN = -13;
const ER_API_DROIT_USAGER = -14;
const ER_API_EMPRUNT_ACTIF = -15;
const ER_API_EMPRUNT_INACTIF = -16;
const ER_API_EMPRUNT_DROIT_COMPTE = -17;
const ER_API_CAPTEUR_OCCUPE = -18;

const OK_NFC_CAPTEUR_UID = 19;
const OK_NFC_CAPTEUR_UID_MANUEL = 20;
const ER_NFC_CAPTEUR_AUTORISATION = -21;
const ER_NFC_CAPTEUR_TIMEOUT = -22;

const G_CODE_ERREURS = {
    [ER_INCONNU]: "Erreur inconnue",
    [OK_RQT_COMPTE_CREA]: "Création du compte réussie",
    [ER_RQT_COMPTE_CREA]: "Création du compte échouée",
    [OK_RQT_COMPTE_CONN]: "Connexion au compte réussie",
    [ER_RQT_COMPTE_CONN]: "Connexion au compte échouée",
    [OK_RQT_COMPTE_SUPP]: "Suppression du compte réussie",
    [ER_RQT_COMPTE_SUPP]: "Suppression du compte échouée",
    [OK_RQT_LIVRE_CREA]: "Ajout du livre réussi",
    [ER_RQT_LIVRE_CREA]: "Ajout du livre échoué",
    [OK_RQT_LIVRE_LIST]: "Listage des livres réussi",
    [ER_RQT_LIVRE_LIST]: "Listage des livres échoué",
    [OK_RQT_LIVRE_SUPP]: "Retrait du livre réussi",
    [ER_RQT_LIVRE_SUPP]: "Retrait du livre échoué",
    [OK_RQT_EMPRUNT_CREA]: "Emprunt réussi",
    [ER_RQT_EMPRUNT_CREA]: "Emprunt échoué",
    [OK_RQT_EMPRUNT_LIST]: "Listage des emprunts par compte réussi",
    [ER_RQT_EMPRUNT_LIST]: "Listage des emprunts par compte échoué",
    [OK_RQT_LIVRE_INFO_UID]: "Obtention des informations par UID réussi",
    [ER_RQT_LIVRE_INFO_UID]: "Obtention des informations par UID échoué",
    [OK_RQT_EMPRUNT_MOD_RETOUR]: "Retour réussi",
    [ER_RQT_EMPRUNT_MOD_RETOUR]: "Retour échoué",
    [OK_API_INFO_CONN]: "Obtention du statut de connexion réussi",
    [ER_API_INFO_CONN]: "Obtention du statut de connexion échoué",
    [OK_API_DECONNECT]: "Déconnexion réussie",
    [ER_API_DROIT_ADMIN]: "Vous n'êtes pas un administrateur",
    [ER_API_DROIT_USAGER]: "Vous n'êtes pas un usager",
    [ER_API_EMPRUNT_ACTIF]: "Livre déjà emprunté",
    [ER_API_EMPRUNT_INACTIF]: "Livre pas emprunté",
    [ER_API_EMPRUNT_DROIT_COMPTE]: "Le livre doit être rendu depuis le compte d'emprunt",
    [ER_API_CAPTEUR_OCCUPE]: "Capteur occupé",
    [OK_NFC_CAPTEUR_UID]: "Obtention de l'UID réussi",
    [OK_NFC_CAPTEUR_UID_MANUEL]: "Obtention de l'UID réussi (manuel)",
    [ER_NFC_CAPTEUR_AUTORISATION]: "Carte verrouillée",
    [ER_NFC_CAPTEUR_TIMEOUT]: "Timeout écoulé"
};

// -------------------- FONCTIONS -------------------- //
function est_un_email(email)
{
    const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex_email.test(email);
}

function aujourdhui_yyyy_mm_dd()
{
    const aujourdhui = new Date();
    const annee = aujourdhui.getFullYear();
    const mois = String(aujourdhui.getMonth() + 1).padStart(2, '0');
    const jour = String(aujourdhui.getDate()).padStart(2, '0');
    const yyyy_mm_dd = `${annee}-${mois}-${jour}`;
    return yyyy_mm_dd;
}

function parametre_get(key) {
    const url_param = new URLSearchParams(window.location.search);
    return url_param.get(key);
}

function construire_requete_get(url, param) {
    const url_param = new URL(url);
    Object.keys(param).forEach(key => url_param.searchParams.append(key, param[key]));
    return url_param;
}

function requete_get(url, param) {
    return fetch(construire_requete_get(window.location.origin + url, param), {
        method: 'GET',
    })
    .then(response => response.json())
    .then(json_data => { return json_data; })
    .catch(error => { console.error('Error:', error); });
}

function requete_post(url, donnees) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donnees),
    })
    .then(response => response.json())
    .then(json_data => { return json_data; })
    .catch(error => { console.error('Error:', error); });
}

function api_statut() {
    return requete_get("/api_statut", {});
}

function api_deconnexion() {
    return requete_post("/api_deconnexion", {});
}

function api_inscription(email, motdepasse, pseudo, date_naissance) {
    return requete_post("/api_inscription", {
        email: email,
        motdepasse: motdepasse,
        pseudo: pseudo,
        naissance: date_naissance
    });
}

function api_connexion(email, motdepasse) {
    return requete_post("/api_connexion", {
        email: email,
        motdepasse: motdepasse,
    });
}

function api_desinscription(email, motdepasse) {
    return requete_post("/api_desinscription", {
        email: email,
        motdepasse: motdepasse,
    });
}

function api_ajout(titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image, image_b64) {
    return requete_post("/api_ajout", {
        titre: titre,
        genre: genre,
        auteur: auteur,
        editeur: editeur,
        rayon: rayon,
        date_parution: date_parution,
        uid_nfc: uid_nfc,
        nom_image: nom_image,
        image_b64: image_b64
    });
}

function api_livres() {
    return requete_get("/api_livres", {});
}

function api_retrait(id_l) {
    return requete_post("/api_retrait", {"id_l": id_l});
}

function api_emprunt(id_l) {
    return requete_post("/api_emprunt", {"id_l": id_l});
}

function api_liste_emprunts() {
    return requete_get("/api_liste_emprunts", {});
}

function api_info_livre(uid_nfc) {
    return requete_get("/api_info_livre", {"uid_nfc": uid_nfc});
}

function api_retour(uid_nfc) {
    return requete_post("/api_retour", {"uid_nfc": uid_nfc});
}

function api_uid_nfc() {
    return requete_get("/api_uid_nfc", {})
}