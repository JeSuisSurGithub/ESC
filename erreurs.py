# Codes erreurs
ER_INCONNU                  =   0
OK_RQT_COMPTE_CREA          =   1
ER_RQT_COMPTE_CREA          =  -1
OK_RQT_COMPTE_CONN          =   2
ER_RQT_COMPTE_CONN          =  -2
OK_RQT_COMPTE_SUPP          =   3
ER_RQT_COMPTE_SUPP          =  -3
OK_RQT_LIVRE_CREA           =   4
ER_RQT_LIVRE_CREA           =  -4
OK_RQT_LIVRE_LIST           =   5
ER_RQT_LIVRE_LIST           =  -5
OK_RQT_LIVRE_SUPP           =   6
ER_RQT_LIVRE_SUPP           =  -6
OK_RQT_EMPRUNT_CREA         =   7
ER_RQT_EMPRUNT_CREA         =  -7
OK_RQT_EMPRUNT_LIST_COMPTE  =   8
ER_RQT_EMPRUNT_LIST_COMPTE  =  -8
OK_RQT_EMPRUNT_LIST_LIVRE   =   9
ER_RQT_EMPRUNT_LIST_LIVRE   =  -9
OK_RQT_EMPRUNT_MOD_RETOUR   =  10
ER_RQT_EMPRUNT_MOD_RETOUR   = -10

OK_API_INFO_CONN            =  11
ER_API_INFO_CONN            = -11
OK_API_DECONNECT            =  12

ER_API_DROIT_ADMIN          = -13
ER_API_DROIT_USAGER         = -14
ER_API_EMPRUNT_ACTIF        = -15
ER_API_EMPRUNT_INACTIF      = -16
ER_API_EMPRUNT_DROIT_COMPTE = -17
ER_API_CAPTEUR_OCCUPE       = -18

OK_NFC_CAPTEUR_UID          =  19
ER_NFC_CAPTEUR_DESACTIVE    = -20
ER_NFC_CAPTEUR_AUTORISATION = -21
ER_NFC_CAPTEUR_TIMEOUT      = -22

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
    OK_RQT_LIVRE_LIST           : "Listage des livres réussi",
    ER_RQT_LIVRE_LIST           : "Listage des livres échoué",
    OK_RQT_LIVRE_SUPP           : "Retrait du livre réussi",
    ER_RQT_LIVRE_SUPP           : "Retrait du livre échoué",
    OK_RQT_EMPRUNT_CREA         : "Emprunt réussi",
    ER_RQT_EMPRUNT_CREA         : "Emprunt échoué",
    OK_RQT_EMPRUNT_LIST_COMPTE  : "Listage des emprunts par compte réussi",
    ER_RQT_EMPRUNT_LIST_COMPTE  : "Listage des emprunts par compte échoué",
    OK_RQT_EMPRUNT_LIST_LIVRE   : "Listage des emprunts par livres réussi",
    ER_RQT_EMPRUNT_LIST_LIVRE   : "Listage des emprunts par livres échoué",
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
    ER_NFC_CAPTEUR_DESACTIVE    : "Capteur désactivé",
    ER_NFC_CAPTEUR_AUTORISATION : "Carte verrouillé",
    ER_NFC_CAPTEUR_TIMEOUT      : "Timeout écoulé"
}