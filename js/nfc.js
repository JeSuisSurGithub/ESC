let temps_limite = 10;
const tag_compteur = document.getElementById("compteur");

const provenance = parametre_get("provenance");
const action = parametre_get("action");

tag_compteur.innerHTML = `Il vous reste ${temps_limite}s...`
let intervalle = setInterval(function () {
    tag_compteur.innerHTML = `Il vous reste ${--temps_limite}s...`
    if (temps_limite == 0) {
        clearInterval(intervalle);

        const redirection = construire_requete_get(decodeURIComponent(provenance), {
            code: ER_NFC_CAPTEUR_TIMEOUT,
            action: action,
        });
        window.location.href = redirection;
    }
}, 1000);

api_uid_nfc().then((requete_uid) => {
    clearInterval(intervalle);
    if (requete_uid.code > 0) {

        const redirection = construire_requete_get(decodeURIComponent(provenance), {
            code: requete_uid.code,
            action: action,
            uid: requete_uid.val
        });
        window.location.href = redirection;
    } else {
        window.alert(G_CODE_ERREURS[requete_uid.code])
    }
});