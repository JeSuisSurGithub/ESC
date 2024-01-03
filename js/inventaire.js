api_statut().then((requete_statut) => {
    if (requete_statut.code > 0) {
        // Connecté
        if (requete_statut.val.grade === 0) {
            // Admin
        } else {
            // Usager
            window.location.href = `${window.location.origin}/accueil.html`
        }
    } else {
        // Pas connecté
        window.location.href = `${window.location.origin}`
    }
});

async function ajout_livre() {
    const tag_titre         = document.getElementById("titre");
    const tag_genre         = document.getElementById("genre");
    const tag_auteur        = document.getElementById("auteur");
    const tag_editeur       = document.getElementById("editeur");
    const tag_rayon         = document.getElementById("rayon");
    const tag_parution      = document.getElementById("date_parution");
    const tag_couverture    = document.getElementById("image_couverture");
    const tag_compteur      = document.getElementById("compteur");

    let info = "";
    if (tag_titre.value.length < 1) {
        info += "Vous devez spécifier le titre\n";
    }
    if (tag_genre.value.length < 1) {
        info += "Vous devez spécifier le genre\n";
    }
    if (tag_auteur.value.length < 1) {
        info += "Vous devez spécifier l'auteur\n";
    }
    if (tag_editeur.value.length < 1) {
        info += "Vous devez spécifier l'éditeur\n";
    }
    if (tag_rayon.value.length < 1) {
        info += "Vous devez spécifier le rayon\n";
    }
    if (tag_parution.value === "" || aujourdhui_yyyy_mm_dd() <= tag_parution.value) {
        info += "Vous devez spécifier une date valide\n";
    }
    if (tag_couverture.files.length < 1) {
        info += "Vous devez fournir une image de couverture\n";
    }
    if (info != "") {
        window.alert(info);
        return;
    }

    let temps_limite = 10;
    let intervalle = setInterval(() => {
        tag_compteur.innerHTML
            = `Veuillez scanner une carte LIBRE à associer au livre (il vous reste ${--temps_limite}s)`;
        if (temps_limite == 0) {
            clearInterval(intervalle);
            tag_compteur.innerHTML = "Temps écoulé, veuillez réinitier la procédure";
        }
    }, 1000);

    const requete_uid = await api_uid_nfc();
    clearInterval(intervalle);
    tag_compteur.innerHTML = "Gestion d'inventaire";
    if (requete_uid.code > 0) {
        const image_couverture = tag_couverture.files[0];

        const lecteur = new FileReader();
        lecteur.onloadend = async function (event) {
            const image_b64 = event.target.result.split(',')[1];
            const res_ajout = await api_ajout_livre(
                tag_titre.value,
                tag_genre.value,
                tag_auteur.value,
                tag_editeur.value,
                tag_rayon.value,
                tag_parution.value,
                requete_uid.val,
                image_couverture.name,
                image_b64
            );
            window.alert(G_CODE_ERREURS[res_ajout.code])
        };
        lecteur.readAsDataURL(image_couverture);
    } else {
        window.alert(G_CODE_ERREURS[requete_uid.code])
    }
}

async function retrait_livre() {
    const tag_compteur      = document.getElementById("compteur");

    let temps_limite = 10;
    let intervalle = setInterval(() => {
        tag_compteur.innerHTML
            = `Veuillez scanner la carte du livre à retirer de la circulation (il vous reste ${--temps_limite}s)`;
        if (temps_limite == 0) {
            clearInterval(intervalle);
            tag_compteur.innerHTML = "Temps écoulé, veuillez réinitier la procédure";
        }
    }, 1000);

    const requete_uid = await api_uid_nfc();
    clearInterval(intervalle);
    tag_compteur.innerHTML = "Gestion d'inventaire";
    if (requete_uid.code > 0) {
        const res_retrait = await api_suppression_livre(requete_uid.val);
        window.alert(G_CODE_ERREURS[res_retrait.code])
    } else {
        window.alert(G_CODE_ERREURS[requete_uid.code])
    }
}