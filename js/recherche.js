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
            const requete_livre = await api_livres();
            if (requete_livre.code > 0) {
                const index = requete_livre.val.uid_nfc.indexOf(parametre_get("uid"))

                if (parametre_get("action") == "emprunt") {
                    if (index !== -1) {
                        const resultat = await api_emprunt(requete_livre.val.id[index]);
                        window.alert(G_CODE_ERREURS[resultat.code]);
                    } else {
                        window.alert("Carte de livre inconnue");
                    }
                } else if (parametre_get("action") == "retour") {
                    if (index !== -1) {
                        const resultat = await api_retour(requete_livre.val.id[index]);
                        window.alert(G_CODE_ERREURS[resultat.code]);
                    } else {
                        window.alert("Carte de livre inconnue");
                    }
                } else {
                    window.alert("Action impossible")
                }
            }
            else {
                window.alert(G_CODE_ERREURS[requete_livre.code]);
            }
        } else {
            window.alert(G_CODE_ERREURS[info_conn.code]);
        }
    } else if (code !== null) {
        window.alert(G_CODE_ERREURS[code]);
    }
}

function recherche(entree, vtitre, vgenre) {
    const termes = entree.split(" ");
    let vid = []

    boucle_ext: for (let i = 0; i < vtitre.length; i++) {
        let titre = vtitre[i];

        for (const terme of termes) {
            if (titre.includes(terme)) {
                vid.push(i);
                continue boucle_ext;
            }
        };

        let genre = vgenre[i];
        for (const terme of termes) {
            if (genre.includes(terme)) {
                vid.push(i);
                continue boucle_ext;
            }
        };
    }
    return vid;
}

// Liste résultats recherche
(async () => {
    const sortie = document.getElementById("liste_resultats")
    const livres = await api_livres();
    if (livres.code > 0) {
        const entree = parametre_get("entree");
        const indices = recherche(entree, livres.val.titre, livres.val.genre);
        if (indices.length === 0) {
            sortie.innerHTML = `
                            <div class="card">
                                <img src="/img/croix.png">
                                <div class="texte">
                                    <p>
                                        Aucun livre correspondant à la recherche
                                    </p>
                                </div>
                            </div>`
        }
        for (let i = 0; i < livres.val.id.length; i++) {
            sortie.innerHTML += `
                            <div class="card">
                                <img src="/upload/${livres.val.nom_image[i]}" >
                                <div class="texte">
                                    <p>
                                        Titre : ${livres.val.titre[i]} <br/>
                                        Genre: ${livres.val.genre[i]} <br/>
                                        Rayon: ${livres.val.rayon[i]} <br/>
                                        Date de Parution: ${livres.val.date_parution[i]} <br/>
                                        <br/>
                                    </p>
                                </div>
                            </div>`
        }
    } else {
        window.alert(G_CODE_ERREURS[livres.code]);
    }
})();
verifier_action();