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

// Statistiques
const palette32 = [
    "#000000","#222034","#45283c","#663931","#8f563b","#df7126",
    "#d9a066","#eec39a","#fbf236","#99e550","#6abe30","#37946e",
    "#4b692f","#524b24","#323c39","#3f3f74","#306082","#5b6ee1",
    "#639bff","#5fcde4","#cbdbfc","#1adeb3","#9badb7","#847e87",
    "#696a6a","#595652","#76428a","#ac3232","#d95763","#d77bba",
    "#8f974a","#8a6f30",
];

(async () => {
    const tag_stats = document.getElementById("stats");
    const emprunts = await api_statut_emprunt();
    if (emprunts.code > 0) {
        if (emprunts.val.genre.length === 0) {
            tag_stats.innerHTML = "Vous n'avez aucun emprunt actif";
        }
        let frequences = {};
        for (let i = 0; i < emprunts.val.genre.length; i++) {
            let genre = emprunts.val.genre[i];
            frequences[genre] = frequences[genre] ? frequences[genre] + 1 : 1;
        }
        let n_emprunt_total = Object.values(frequences).reduce((total, val) => total + val, 0);
        for (let i = 0; i < Object.keys(frequences).length; i++) {
            tag_stats.innerHTML += `
                <div class="genre">
                    <div class="genre-name" style="font-weight: bold;">${Object.keys(frequences)[i]}</div>
                    <div class="genre-level">
                        <div style="background-color: ${palette32[i]}; width: ${(Object.values(frequences)[i] / n_emprunt_total) * 100}%;" class="genre-percent"></div>
                    </div>
                </div>`;
        }
    } else {
        window.alert(G_CODE_ERREURS[emprunts.code]);
    }
})();