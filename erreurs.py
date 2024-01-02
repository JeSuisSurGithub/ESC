# Défini les codes erreurs et leur messages associés

ER_INCONNU                  =   0

OK_RQT_COMPTE_CREA          =   1
ER_RQT_COMPTE_CREA          =  -1
OK_RQT_COMPTE_CONN          =   2
ER_RQT_COMPTE_CONN          =  -2
OK_RQT_COMPTE_SUPP          =   3
ER_RQT_COMPTE_SUPP          =  -3

OK_RQT_LIVRE_CREA           =   4
ER_RQT_LIVRE_CREA           =  -4
OK_RQT_LIVRE_INFO_UID       =   5
ER_RQT_LIVRE_INFO_UID       =  -5
OK_RQT_LIVRE_RECHERCHE      =   6
ER_RQT_LIVRE_RECHERCHE      =  -6
OK_RQT_LIVRE_SUPP           =   7
ER_RQT_LIVRE_SUPP           =  -7

OK_RQT_EMPRUNT_CREA         =   8
ER_RQT_EMPRUNT_CREA         =  -8
OK_RQT_EMPRUNT_LIST         =   9
ER_RQT_EMPRUNT_LIST         =  -9
OK_RQT_LIVRE_DISPO          =  10
ER_RQT_LIVRE_DISPO          = -10
OK_RQT_EMPRUNT_MOD_RETOUR   =  11
ER_RQT_EMPRUNT_MOD_RETOUR   = -11

OK_API_INFO_CONN            =  12
ER_API_INFO_CONN            = -12
OK_API_DECONNECT            =  13

ER_API_DROIT_ADMIN          = -14
ER_API_DROIT_USAGER         = -15
ER_API_LIVRE_SUPP_NON_LIBRE = -16
ER_API_EMPRUNT_ACTIF        = -17
ER_API_EMPRUNT_INACTIF      = -18
ER_API_EMPRUNT_DROIT_COMPTE = -19
ER_API_CAPTEUR_OCCUPE       = -20

OK_NFC_CAPTEUR_UID          =  21
OK_NFC_CAPTEUR_UID_MANUEL   =  22
ER_NFC_CAPTEUR_AUTORISATION = -23
ER_NFC_CAPTEUR_TIMEOUT      = -24

G_CODE_ERREURS = {
    ER_INCONNU                  : "Erreur inconnue",

    OK_RQT_COMPTE_CREA          : "Création du compte réussie",
    ER_RQT_COMPTE_CREA          : "Création du compte échouée",
    OK_RQT_COMPTE_CONN          : "Connexion au compte réussie",
    ER_RQT_COMPTE_CONN          : "Connexion au compte échouée",
    OK_RQT_COMPTE_SUPP          : "Suppression du compte réussie",
    ER_RQT_COMPTE_SUPP          : "Suppression du compte échouée",

    OK_RQT_LIVRE_CREA           : "Ajout du livre réussi",
    ER_RQT_LIVRE_CREA           : "Ajout du livre échoué",
    OK_RQT_LIVRE_INFO_UID       : "Obtention des informations par UID réussi",
    ER_RQT_LIVRE_INFO_UID       : "Obtention des informations par UID échoué",
    OK_RQT_LIVRE_RECHERCHE      : "Recherche de livre réussie",
    ER_RQT_LIVRE_RECHERCHE      : "Recherche de livre échouée",
    OK_RQT_LIVRE_SUPP           : "Retrait du livre réussi",
    ER_RQT_LIVRE_SUPP           : "Retrait du livre échoué",

    OK_RQT_EMPRUNT_CREA         : "Emprunt réussi",
    ER_RQT_EMPRUNT_CREA         : "Emprunt échoué",
    OK_RQT_EMPRUNT_LIST         : "Listage des emprunts par compte réussi",
    ER_RQT_EMPRUNT_LIST         : "Listage des emprunts par compte échoué",
    OK_RQT_LIVRE_DISPO          : "Obtention du statut d'emprunt réussi",
    ER_RQT_LIVRE_DISPO          : "Obtention du statut d'emprunt échoué",
    OK_RQT_EMPRUNT_MOD_RETOUR   : "Retour réussi",
    ER_RQT_EMPRUNT_MOD_RETOUR   : "Retour échoué",

    OK_API_INFO_CONN            : "Obtention du statut de connexion réussi",
    ER_API_INFO_CONN            : "Obtention du statut de connexion échoué",
    OK_API_DECONNECT            : "Déconnexion réussie",

    ER_API_DROIT_ADMIN          : "Vous n'êtes pas un administrateur",
    ER_API_DROIT_USAGER         : "Vous n'êtes pas un usager",
    ER_API_EMPRUNT_ACTIF        : "Livre déja emprunté",
    ER_API_EMPRUNT_INACTIF      : "Livre pas emprunté",
    ER_API_EMPRUNT_DROIT_COMPTE : "Le livre doit être rendu depuis le compte d'emprunt",
    ER_API_CAPTEUR_OCCUPE       : "Capteur occupé",

    OK_NFC_CAPTEUR_UID          : "Obtention de l'UID réussi",
    OK_NFC_CAPTEUR_UID_MANUEL   : "Obtention du l'UID réussi (manuel)",
    ER_NFC_CAPTEUR_AUTORISATION : "Carte verrouillé",
    ER_NFC_CAPTEUR_TIMEOUT      : "Timeout écoulé"
}