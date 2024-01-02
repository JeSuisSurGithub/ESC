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
const OK_RQT_LIVRE_INFO_UID = 5;
const ER_RQT_LIVRE_INFO_UID = -5;
const OK_RQT_LIVRE_RECHERCHE = 6;
const ER_RQT_LIVRE_RECHERCHE = -6;
const OK_RQT_LIVRE_SUPP = 7;
const ER_RQT_LIVRE_SUPP = -7;

const OK_RQT_EMPRUNT_CREA = 8;
const ER_RQT_EMPRUNT_CREA = -8;
const OK_RQT_EMPRUNT_LIST = 9;
const ER_RQT_EMPRUNT_LIST = -9;
const OK_RQT_LIVRE_DISPO = 10;
const ER_RQT_LIVRE_DISPO = -10;
const OK_RQT_EMPRUNT_MOD_RETOUR = 11;
const ER_RQT_EMPRUNT_MOD_RETOUR = -11;

const OK_API_INFO_CONN = 12;
const ER_API_INFO_CONN = -12;
const OK_API_DECONNECT = 13;

const ER_API_DROIT_ADMIN = -14;
const ER_API_DROIT_USAGER = -15;
const ER_API_LIVRE_SUPP_NON_LIBRE = -16;
const ER_API_EMPRUNT_ACTIF = -17;
const ER_API_EMPRUNT_INACTIF = -18;
const ER_API_EMPRUNT_DROIT_COMPTE = -19;
const ER_API_CAPTEUR_OCCUPE = -20;

const OK_NFC_CAPTEUR_UID = 21;
const OK_NFC_CAPTEUR_UID_MANUEL = 22;
const ER_NFC_CAPTEUR_AUTORISATION = -23;
const ER_NFC_CAPTEUR_TIMEOUT = -24;

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
    [OK_RQT_LIVRE_INFO_UID]: "Obtention des informations par UID réussi",
    [ER_RQT_LIVRE_INFO_UID]: "Obtention des informations par UID échoué",
    [OK_RQT_LIVRE_RECHERCHE]: "Recherche de livre réussie",
    [ER_RQT_LIVRE_RECHERCHE]: "Recherche de livre échouée",
    [OK_RQT_LIVRE_SUPP]: "Retrait du livre réussi",
    [ER_RQT_LIVRE_SUPP]: "Retrait du livre échoué",

    [OK_RQT_EMPRUNT_CREA]: "Emprunt réussi",
    [ER_RQT_EMPRUNT_CREA]: "Emprunt échoué",
    [OK_RQT_EMPRUNT_LIST]: "Listage des emprunts par compte réussi",
    [ER_RQT_EMPRUNT_LIST]: "Listage des emprunts par compte échoué",
    [OK_RQT_LIVRE_DISPO]: "Obtention du statut d'emprunt réussi",
    [ER_RQT_LIVRE_DISPO]: "Obtention du statut d'emprunt échoué",
    [OK_RQT_EMPRUNT_MOD_RETOUR]: "Retour réussi",
    [ER_RQT_EMPRUNT_MOD_RETOUR]: "Retour échoué",

    [OK_API_INFO_CONN]: "Obtention du statut de connexion réussi",
    [ER_API_INFO_CONN]: "Obtention du statut de connexion échoué",
    [OK_API_DECONNECT]: "Déconnexion réussie",

    [ER_API_DROIT_ADMIN]: "Vous n'êtes pas un administrateur",
    [ER_API_DROIT_USAGER]: "Vous n'êtes pas un usager",
    [ER_API_EMPRUNT_ACTIF]: "Livre déjà emprunté",
    [ER_API_EMPRUNT_INACTIF]: "Livre non emprunté",
    [ER_API_EMPRUNT_DROIT_COMPTE]: "Le livre doit être rendu depuis le compte d'emprunt",
    [ER_API_CAPTEUR_OCCUPE]: "Capteur occupé",

    [OK_NFC_CAPTEUR_UID]: "Obtention de l'UID réussi",
    [OK_NFC_CAPTEUR_UID_MANUEL]: "Obtention du l'UID réussi (manuel)",
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

function construire_requete_get(url_complete, param) {
    const url_param = new URL(url_complete);
    Object.keys(param).forEach(key => url_param.searchParams.append(key, param[key]));
    return url_param;
}

function requete_get(url_suffixe, param) {
    return fetch(construire_requete_get(window.location.origin + url_suffixe, param), {
        method: 'GET',
    })
    .then(response => response.json())
    .then(json_data => { return json_data; })
    .catch(error => { console.error('Error:', error); });
}

function requete_post(url_suffixe, donnees) {
    return fetch(window.location.origin + url_suffixe, {
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
    return requete_get("/api_deconnexion", {});
}

function api_inscription(email, motdepasse, pseudo, date_naissance) {
    return requete_post("/api_inscription", {
        email, motdepasse, pseudo, naissance
    });
}

function api_connexion(email, motdepasse) {
    return requete_post("/api_connexion", {
        email, motdepasse,
    });
}

function api_desinscription(email, motdepasse) {
    return requete_post("/api_desinscription", {
        email, motdepasse,
    });
}

function api_ajout_livre(titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image, image_b64) {
    return requete_post("/api_ajout_livre", {
        titre, genre, auteur, editeur, rayon, date_parution, uid_nfc, nom_image, image_b64
    });
}

function api_info_livre(uid_nfc) {
    return requete_get("/api_info_livre", {uid_nfc});
}

function api_recherche_livre(termes) {
    return requete_post("/api_recherche_livre", {termes});
}

function api_suppression_livre(uid_nfc) {
    return requete_post("/api_suppression_livre", {uid_nfc});
}

function api_emprunt(uid_nfc) {
    return requete_post("/api_emprunt", {uid_nfc});
}

function api_liste_emprunts() {
    return requete_get("/api_liste_emprunts", {});
}

function api_info_emprunt(uid_nfc) {
    return requete_get("/api_info_emprunt", {uid_nfc});
}

function api_retour(uid_nfc) {
    return requete_post("/api_retour", {uid_nfc});
}

function api_uid_nfc() {
    return requete_get("/api_uid_nfc", {})
}