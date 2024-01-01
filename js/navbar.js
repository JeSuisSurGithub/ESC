// Recherche
document.addEventListener("DOMContentLoaded", function() {
    let searchBtn = document.querySelector('.searchBtn');
    let closeBtn = document.querySelector('.closeBtn');
    let searchBox = document.querySelector('.searchBox');
    let inputField = document.getElementById('valeurs');

    searchBtn.onclick = function() {
        if (searchBtn.classList.contains('active') && inputField.value.trim() !== '') {
            const url = construire_requete_get(`${window.location.origin}/html/recherche.html`, {
                entree: encodeURIComponent(inputField.value)
            });
            window.location.href = url;
        }

        searchBox.classList.add('active');
        closeBtn.classList.add('active');
        searchBtn.classList.add('active');
    }

    closeBtn.onclick = function() {
        searchBox.classList.remove('active');
        closeBtn.classList.remove('active');
        searchBtn.classList.remove('active');
    }
});

// Actions
async function deconnexion() {
    await api_deconnexion();
    window.location.href = window.location.origin;
}

async function emprunter() {
    const redirection = construire_requete_get(`${window.location.origin}/html/nfc.html`, {
        provenance: `${encodeURIComponent(window.location.href.split("?")[0])}`,
        action: "emprunt",
    });
    window.location.href = redirection;
}

async function retour() {
    const redirection = construire_requete_get(`${window.location.origin}/html/nfc.html`, {
        provenance: `${encodeURIComponent(window.location.href.split("?")[0])}`,
        action: "retour",
    });
    window.location.href = redirection;
}

async function verifier_action() {
    const code = parametre_get("code");
    if (code > 0) {
        const info_conn = await api_statut();
        if (info_conn.code > 0) {
            if (parametre_get("action") === "emprunt") {
                const requete_livre = await api_livres();
                if (requete_livre.code > 0) {
                    const index = requete_livre.val.uid_nfc.indexOf(parametre_get("uid"));
                    if (index !== -1) {
                        const resultat = await api_emprunt(requete_livre.val.id[index]);
                        window.alert(G_CODE_ERREURS[resultat.code]);
                        window.location.href = window.location.href.split("?")[0];
                    } else {
                        window.alert("Carte de livre inconnue");
                    }
                }
                else {
                    window.alert(G_CODE_ERREURS[requete_livre.code]);
                }
            }
            else if (parametre_get("action") == "retour") {
                if (index !== -1) {
                    const resultat = await api_retour(parametre_get("uid"));
                    window.alert(G_CODE_ERREURS[resultat.code]);
                    window.location.href = window.location.href.split("?")[0];
                } else {
                    window.alert("Carte de livre inconnue");
                }
            } else {
                window.alert("Action impossible")
            }
        } else {
            window.alert(G_CODE_ERREURS[info_conn.code]);
        }
    } else if (code !== null) {
        window.alert(G_CODE_ERREURS[code]);
    }
}

verifier_action();