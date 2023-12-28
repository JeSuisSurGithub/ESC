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
                        window.location.href = window.location.href.split("?")[0];
                    } else {
                        window.alert("Carte de livre inconnue");
                    }
                } else if (parametre_get("action") == "retour") {
                    if (index !== -1) {
                        const resultat = await api_retour(requete_livre.val.id[index]);
                        window.alert(G_CODE_ERREURS[resultat.code]);
                        window.location.href = window.location.href.split("?")[0];
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

// Liste emprunts
(async () => {
    const sortie = document.getElementById("liste_emprunts")
    const livres_empruntes = await api_statut_emprunt();
    if (livres_empruntes.code > 0) {
        if (livres_empruntes.val.id_l.length === 0) {
            sortie.innerHTML = `
                            <div class="card">
                                <img src="/img/croix.png">
                                <div class="texte">
                                    <p>
                                        Vous n'avez aucun emprunt actif
                                    </p>
                                </div>
                            </div>`
        }
        for (let i = 0; i < livres_empruntes.val.id_l.length; i++) {
            if (livres_empruntes.val.rendu[i] === 0) {
                sortie.innerHTML += `
                                <div class="card">
                                    <img src="/upload/${livres_empruntes.val.nom_image[i]}" >
                                    <div class="texte">
                                        <p>
                                            Titre : ${livres_empruntes.val.titre[i]} <br/>
                                            Genre: ${livres_empruntes.val.genre[i]} <br/>
                                            Date d'emprunt: ${livres_empruntes.val.date_debut[i]} <br/>
                                            Date de retour: ${livres_empruntes.val.date_fin[i]} <br/>
                                            <br/>
                                        </p>
                                    </div>
                                </div>`
            }
        }
    } else {
        window.alert(G_CODE_ERREURS[livres_empruntes.code]);
    }
})();
verifier_action();

// Calendrier
const header = document.querySelector(".calendar h3");
const dates = document.querySelector(".dates");
const navs = document.querySelectorAll("#prev, #next");

const months = [
    "Janvier",
    "Fevrier",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Decembre",
];

let date = new Date();
let month = date.getMonth();
let year = date.getFullYear();

function render_calendar() {
    const start = new Date(year, month, 1).getDay();
    const endDate = new Date(year, month + 1, 0).getDate();
    const end = new Date(year, month, endDate).getDay();
    const endDatePrev = new Date(year, month, 0).getDate();

    let datesHtml = "";

    for (let i = start; i > 0; i--) {
        datesHtml += `<li class="inactive">${endDatePrev - i + 1}</li>`;
    }

    for (let i = 1; i <= endDate; i++) {
        let className =
        i === date.getDate() &&
        month === new Date().getMonth() &&
        year === new Date().getFullYear()
            ? ' class="today"'
            : "";
        datesHtml += `<li${className}>${i}</li>`;
    }

    for (let i = end; i < 6; i++) {
        datesHtml += `<li class="inactive">${i - end + 1}</li>`;
    }

    dates.innerHTML = datesHtml;
    header.textContent = `${months[month]} ${year}`;
}

navs.forEach((nav) => {
    nav.addEventListener("click", (e) => {
        const btnId = e.target.id;

        if (btnId === "prev" && month === 0) {
            year--;
            month = 11;
        } else if (btnId === "next" && month === 11) {
            year++;
            month = 0;
        } else {
            month = btnId === "next" ? month + 1 : month - 1;
        }

        date = new Date(year, month, new Date().getDate());
        year = date.getFullYear();
        month = date.getMonth();

        render_calendar();
    });
});
render_calendar();