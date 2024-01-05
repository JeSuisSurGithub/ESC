const palette32 = [
    "#d9a066", "#4b692f", "#639bff", "#696a6a", "#8f974a", "#000000",
    "#222034", "#eec39a", "#524b24", "#5fcde4", "#595652", "#8a6f30",
    "#45283c", "#fbf236", "#323c39", "#cbdbfc", "#76428a", "#663931",
    "#99e550", "#3f3f74", "#1adeb3", "#ac3232", "#8f563b", "#6abe30",
    "#306082", "#9badb7", "#d95763", "#df7126", "#37946e", "#5b6ee1",
    "#847e87", "#d77bba",
];

api_statut().then((requete_statut) => {
    if (requete_statut.code > 0) {
        // Connecté
        if (requete_statut.val.grade === 0) {
            // Admin
            window.location.href = `${window.location.origin}/html/inventaire.html`
        } else {
            // Usager
            api_liste_emprunts().then((requete_emprunts) => {
                if (requete_emprunts.code > 0) {
                    const n_emprunts = requete_emprunts.val.titre.length;
                    // Affichage emprunts
                    {
                        const tag_liste_emprunts = document.getElementById("liste_emprunts")
                        // Si aucun emprunt ou tout emprunts rendu
                        if (requete_emprunts.val.rendu.reduce((total, val) => total + val, 0) === n_emprunts) {
                            tag_liste_emprunts.innerHTML = `
                                            <div class="card">
                                                <img src="/img/croix.png">
                                                <div class="texte">
                                                    <p>
                                                        Vous n'avez aucun emprunt actif
                                                    </p>
                                                </div>
                                            </div>`
                        } else {
                            for (let i = 0; i < n_emprunts; i++) {
                                if (requete_emprunts.val.rendu[i] === 0) {
                                    tag_liste_emprunts.innerHTML += `
                                                    <div class="card">
                                                        <img src="/upload/${requete_emprunts.val.nom_image[i]}" >
                                                        <div class="texte">
                                                            <p>
                                                                Titre : ${requete_emprunts.val.titre[i]} <br/>
                                                                Genre: ${requete_emprunts.val.genre[i]} <br/>
                                                                Auteur: ${requete_emprunts.val.auteur[i]} <br/>
                                                                Editeur: ${requete_emprunts.val.editeur[i]} <br/>
                                                                Date de Parution: ${requete_emprunts.val.date_parution[i]} <br/>
                                                                Date d'emprunt: ${requete_emprunts.val.date_debut[i]} <br/>
                                                                Date de retour: ${requete_emprunts.val.date_fin[i]} <br/>
                                                                <br/>
                                                            </p>
                                                        </div>
                                                    </div>`
                                }
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
                            const genre = requete_emprunts.val.genre[i];
                            frequences[genre] = frequences[genre] ? frequences[genre] + 1 : 1;
                        }
                        for (let i = 0; i < Object.keys(frequences).length; i++) {
                            const pourcentage = (Object.values(frequences)[i] / n_emprunts) * 100;
                            tag_stats.innerHTML += `
                                <div class="genre">
                                    <div class="genre-name" style="font-weight: bold;">${Object.keys(frequences)[i]}</div>
                                    <div class="genre-level">
                                        <div style="background-color: ${palette32[i]}; width: ${pourcentage}%;" class="genre-percent"></div>
                                    </div>
                                </div>`;
                        }
                    }
                } else {
                    window.alert(G_CODE_ERREURS[requete_emprunts.code]);
                }
            });

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
        }
    } else {
        // Pas connecté
        window.location.href = `${window.location.origin}`
    }
});

