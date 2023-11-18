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

est_connecte()
    .then(info_statut => {
        let msg_connect = info_statut.resultat ? "Connecté" : "Pas connecté";
        document.getElementById("info_statut").innerHTML = `<p>${msg_connect}, Grade: ${info_statut.grade}</p><br/>`;
    })
    .catch(error => {
        document.getElementById("info_statut").innerHTML = `<p>Statut de connexion indisponible (${error.message})</p><br/>`;
    });