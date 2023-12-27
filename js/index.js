document.addEventListener("DOMContentLoaded", function() {
    let searchBtn = document.querySelector('.searchBtn');
    let closeBtn = document.querySelector('.closeBtn');
    let searchBox = document.querySelector('.searchBox');
    let inputField = document.getElementById('valeurs');

    searchBtn.onclick = function() {
        searchBox.classList.add('active');
        closeBtn.classList.add('active');
        searchBtn.classList.add('active');

        if (searchBtn.classList.contains('active') && inputField.value.trim() !== '') {
            console.log("cliquer deux fois");
        }
    }

    closeBtn.onclick = function() {
        searchBox.classList.remove('active');
        closeBtn.classList.remove('active');
        searchBtn.classList.remove('active');
    }
});

document.addEventListener("DOMContentLoaded", function() {
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

function renderCalendar() {
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

    renderCalendar();
  });
});

renderCalendar();});

function est_un_email(email)
{
    const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex_email.test(email);
}

function aujourdhui_yyyy_mm_dd()
{
    const aujourdhui = new Date();
    const annee = aujourdhui.getFullYear();
    const mois = String(aujourdhui.getMonth() + 1).padStart(2, '0');
    const jour = String(aujourdhui.getDate()).padStart(2, '0');
    const yyyy_mm_dd = `${annee}-${mois}-${jour}`;
    return yyyy_mm_dd;
}

function parametre_get(key) {
    const url_param = new URLSearchParams(window.location.search);
    return url_param.get(key);
}

function construire_requete_get(url, param) {
    const url_param = new URL(url);
    Object.keys(param).forEach(key => url_param.searchParams.append(key, param[key]));
    return url_param;
}

function requete_get(url, param) {
    return fetch(construire_requete_get(window.location.origin + url, param), {
        method: 'GET',
    })
    .then(response => response.json())
    .then(json_data => { return json_data; })
    .catch(error => { console.error('Error:', error); });
}

function requete_post(url, donnees) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donnees),
    })
    .then(response => response.json())
    .then(json_data => { return json_data; })
    .catch(error => { console.error('Error:', error); });
}

function api_statut() {
    return requete_get("/api_statut", {});
}

function api_deconnexion() {
    return requete_post("/api_deconnexion", {});
}

function api_inscription(email, motdepasse, pseudo, date_naissance) {
    return requete_post("/api_inscription", {
        email: email,
        motdepasse: motdepasse,
        pseudo: pseudo,
        naissance: date_naissance
    });
}

function api_connexion(email, motdepasse) {
    return requete_post("/api_connexion", {
        email: email,
        motdepasse: motdepasse,
    });
}

function api_desinscription(email, motdepasse) {
    return requete_post("/api_desinscription", {
        email: email,
        motdepasse: motdepasse,
    });
}

function api_ajout(titre, genre, rayon, date_parution, guid_nfc) {
    return requete_post("/api_ajout", {
        titre: titre,
        genre: genre,
        rayon: rayon,
        date_parution: date_parution,
        guid_nfc: guid_nfc,
    });
}

function api_livres() {
    return requete_get("/api_livres", {});
}

function api_retrait(id_l) {
    return requete_post("/api_retrait", {"id_l": id_l});
}

function api_emprunt(id_l) {
    return requete_post("/api_emprunt", {"id_l": id_l});
}

function api_emprunt_livres() {
    return requete_get("/api_emprunt_livres", {});
}

function api_hist_livre(id_l) {
    return requete_get("/api_hist_livre", {"id_l": id_l});
}

function api_retour(id_l) {
    return requete_post("/api_retour", {"id_l": id_l});
}

function api_uid_nfc() {
    return requete_get("/api_uid_nfc", {})
}

function recherche(entree, vtitre, vgenre, vdate) {
    const termes = entree.split(" ");
    var vid = []

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

        let date = vdate[i];
        for (const terme of termes) {
            if (date.includes(terme)) {
                vid.push(i);
                continue boucle_ext;
            }
        };
    }
    return vid;
}

