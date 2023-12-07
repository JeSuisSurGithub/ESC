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

function est_connecte() {
    return new Promise((resolve, reject) => {
        fetch('/sql_statut')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Request failed');
                }
                return response.json();
            })
            .then(data => resolve(data))
            .catch(error => reject(error));
    });
}

function connexion()
{
    var tag_email = document.getElementById("email");
    var tag_motdepasse = document.getElementById("motdepasse");
    var tag_info = document.getElementById("info_erreurs");

    tag_info.innerHTML = "";
    if (!est_un_email(tag_email.value)) {
        tag_info.innerHTML += "<p>L'email n'est pas valide</p>";
    }
    if (tag_motdepasse.value.length < 4) {
        tag_info.innerHTML += "<p>Le mot de passe doit faire au moins de 4 caractères</p>";
    }
    if (tag_info.innerHTML != "") return;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            tag_info.innerHTML = reponse.resultat ? "La connexion a réussi" : "La connexion a échoué";
        }
    };

    xhr.open('POST', "/sql_connexion", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        {
            email: email.value,
            motdepasse: motdepasse.value,
        }
    ));
}

function deconnexion(silence = false)
{
    var tag_info = document.getElementById("info_erreurs");
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            if (silence === false) {
                tag_info.innerHTML = reponse.resultat ? "La déconnexion a réussi" : "La déconnexion a échoué";
            }
        }
    };

    xhr.open('POST', "/sql_deconnexion", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function sinscrire()
{
    var tag_email = document.getElementById("email");
    var tag_motdepasse = document.getElementById("motdepasse");
    var tag_nom = document.getElementById("nom");
    var tag_prenom = document.getElementById("prenom");
    var tag_naissance = document.getElementById("naissance");
    var tag_info = document.getElementById("info_erreurs");

    tag_info.innerHTML = "";
    if (!est_un_email(tag_email.value)) {
        tag_info.innerHTML += "<p>L'email n'est pas valide</p>";
    }
    if (tag_motdepasse.value.length < 4) {
        tag_info.innerHTML += "<p>Le mot de passe doit faire au moins de 4 caractères</p>";
    }
    if (tag_nom.value.length < 1) {
        tag_info.innerHTML += "<p>Vous devez spécifier un nom</p>";
    }
    if (tag_prenom.value.length < 1) {
        tag_info.innerHTML += "<p>Vous devez spécifier un prénom</p>";
    }
    if (tag_naissance.value == "" || aujourdhui_yyyy_mm_dd() <= tag_naissance.value) {
        tag_info.innerHTML += "<p>Date invalide</p>";
    }
    if (tag_info.innerHTML != "") return;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            tag_info.innerHTML = reponse.resultat ? "L'inscription a réussi" : "L'inscription a échoué";
        }
    };

    xhr.open('POST', "/sql_inscription", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        {
            email: tag_email.value,
            motdepasse: tag_motdepasse.value,
            nom: tag_nom.value,
            prenom: tag_prenom.value,
            naissance: tag_naissance.value
        }
    ));
}

function supprimer()
{
    var tag_email = document.getElementById("email");
    var tag_motdepasse = document.getElementById("motdepasse");
    var tag_info = document.getElementById("info_erreurs");

    tag_info.innerHTML = "";
    if (!est_un_email(tag_email.value)) {
        tag_info.innerHTML += "<p>L'email n'est pas valide</p>";
    }
    if (tag_motdepasse.value.length < 4) {
        tag_info.innerHTML += "<p>Le mot de passe doit faire au moins de 4 caractères</p>";
    }
    if (tag_info.innerHTML != "") return;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            deconnexion({silence: true});
            tag_info.innerHTML += reponse.resultat ? "La suppression a réussi" : "La suppression a échoué";
        }
    };

    xhr.open('POST', "/sql_desinscription", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        {
            email: email.value,
            motdepasse: motdepasse.value,
        }
    ));
}

function liste_livres(empruntes) {
    return new Promise((resolve, reject) => {
        fetch(empruntes ? '/sql_livres_empruntes' : '/sql_livres')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Request failed');
                }
                return response.json();
            })
            .then(data => resolve(data))
            .catch(error => reject(error));
    });
}