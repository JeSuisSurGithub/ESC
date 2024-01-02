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

async function desinscription() {
    window.location.href = `${window.location.origin}/html/desinscription.html`;
}

async function emprunt() {
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
        if (parametre_get("action") === "emprunt") {
            const requete_emprunt = await api_emprunt(parametre_get("uid"));
            window.alert(G_CODE_ERREURS[requete_emprunt.code]);
            window.location.href = window.location.href.split("?")[0];
        }
        else if (parametre_get("action") === "retour") {
            const requete_retour = await api_retour(parametre_get("uid"));
            window.alert(G_CODE_ERREURS[requete_retour.code]);
            window.location.href = window.location.href.split("?")[0];
        } else {
            window.alert("Action impossible")
        }
    } else if (code !== null) {
        window.alert(G_CODE_ERREURS[code]);
    }
}

verifier_action();