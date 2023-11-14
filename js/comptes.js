var EST_CONNECTE = false;

function est_connecte()
{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200)
        {
            EST_CONNECTE = JSON.parse(this.responseText);
        }
    };

    xhr.open('GET', "/sql_est_connecte", true);
    xhr.send();
}

function sinscrire()
{
    var xhr = new XMLHttpRequest();
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            // Réussi!
        }
    };

    xhr.open('POST', "/sql_inscription", true);
    xhr.send(JSON.stringify(
        {
            nom_u: document.getElementById("nom_u").value,
            motdepasse: document.getElementById("motdepasse").value
        }
    ));
}

function connexion()
{
    var xhr = new XMLHttpRequest();
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200)
        {
            var reponse = JSON.parse(this.responseText);
            // Réussi!
        }
    };

    xhr.open('POST', "/sql_connexion", true);
    xhr.send(JSON.stringify(
        {
            nom_u: document.getElementById("nom_u").value,
            motdepasse: document.getElementById("motdepasse").value
        }
    ));
}