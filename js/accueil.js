const palette32 = [
    "#000000", "#d9a066", "#4b692f", "#639bff", "#696a6a", "#8f974a",
    "#222034", "#eec39a", "#524b24", "#5fcde4", "#595652", "#8a6f30",
    "#45283c", "#fbf236", "#323c39", "#cbdbfc", "#76428a", "#663931",
    "#99e550", "#3f3f74", "#1adeb3", "#ac3232", "#8f563b", "#6abe30",
    "#306082", "#9badb7", "#d95763", "#df7126", "#37946e", "#5b6ee1",
    "#847e87", "#d77bba",
];

// Liste emprunts
(async () => {
    const emprunts = await api_liste_emprunts();
    if (emprunts.code > 0) {
        // Affichage
        {
            const sortie = document.getElementById("liste_emprunts")
            let n_emprunts = emprunts.val.titre.length;
            // Si aucun emprunt ou tout emprunts rendu
            if (n_emprunts === 0 || emprunts.val.rendu.reduce((total, val) => total + val, 0) === n_emprunts) {
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
            for (let i = 0; i < n_emprunts; i++) {
                if (emprunts.val.rendu[i] === 0) {
                    sortie.innerHTML += `
                                    <div class="card">
                                        <img src="/upload/${emprunts.val.nom_image[i]}" >
                                        <div class="texte">
                                            <p>
                                                Titre : ${emprunts.val.titre[i]} <br/>
                                                Genre: ${emprunts.val.genre[i]} <br/>
                                                Auteur: ${emprunts.val.auteur[i]} <br/>
                                                Editeur: ${emprunts.val.editeur[i]} <br/>
                                                Date de Parution: ${emprunts.val.date_parution[i]} <br/>
                                                Date d'emprunt: ${emprunts.val.date_debut[i]} <br/>
                                                Date de retour: ${emprunts.val.date_fin[i]} <br/>
                                                <br/>
                                            </p>
                                        </div>
                                    </div>`
                }
            }
        }

        // Stats
        {
            const tag_stats = document.getElementById("stats");
            if (n_emprunts === 0) {
                tag_stats.innerHTML = "Vous n'avez aucun emprunt";
            }
            let frequences = {};
            for (let i = 0; i < n_emprunts; i++) {
                let genre = emprunts.val.genre[i];
                frequences[genre] = frequences[genre] ? frequences[genre] + 1 : 1;
            }
            for (let i = 0; i < Object.keys(frequences).length; i++) {
                tag_stats.innerHTML += `
                    <div class="genre">
                        <div class="genre-name" style="font-weight: bold;">${Object.keys(frequences)[i]}</div>
                        <div class="genre-level">
                            <div style="background-color: ${palette32[i]}; width: ${(Object.values(frequences)[i] / n_emprunts) * 100}%;" class="genre-percent"></div>
                        </div>
                    </div>`;
            }
        }
    } else {
        window.alert(G_CODE_ERREURS[emprunts.code]);
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