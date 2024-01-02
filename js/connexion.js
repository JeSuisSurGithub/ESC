async function inscription() {
    const tag_email = document.getElementById("email_inscription");
    const tag_motdepasse = document.getElementById("motdepasse_inscription");
    const tag_pseudo = document.getElementById("pseudo");
    const tag_naissance = document.getElementById("naissance");

    let info = "";
    if (!est_un_email(tag_email.value)) {
        info += "L'email n'est pas valide\n";
    }
    if (tag_motdepasse.value.length < 4) {
        info += "Le mot de passe doit faire au moins de 4 caractères\n";
    }
    if (tag_pseudo.value.length < 1) {
        info += "Vous devez spécifier un pseudo\n";
    }
    if (tag_naissance.value == "" || aujourdhui_yyyy_mm_dd() <= tag_naissance.value) {
        info += "Date invalide\n";
    }
    if (info != "") {
        window.alert(info);
        return;
    }

    const requete_inscription = await api_inscription(tag_email.value, tag_motdepasse.value, tag_pseudo.value, tag_naissance.value);
    if (requete_inscription.code > 0) {
        const requete_connexion = await api_connexion(tag_email.value, tag_motdepasse.value);
        if (requete_connexion.code > 0) {
            window.location.href = `${window.location.origin}/html/accueil.html`;
        } else {
            window.alert(G_CODE_ERREURS[requete_connexion.code]);
        }
    } else {
        window.alert(G_CODE_ERREURS[requete_inscription.code]);
    }
}

async function connexion() {
    const tag_email = document.getElementById("email_connexion");
    const tag_motdepasse = document.getElementById("motdepasse_connexion");

    let info = "";
    if (!est_un_email(tag_email.value)) {
        info += "L'email n'est pas valide\n";
    }
    if (tag_motdepasse.value.length < 4) {
        info += "Le mot de passe doit faire au moins de 4 caractères\n";
    }
    if (info != "") {
        window.alert(info);
        return;
    }

    const requete_connexion = await api_connexion(tag_email.value, tag_motdepasse.value);
    if (requete_connexion.code > 0) {
        window.location.href = `${window.location.origin}/html/accueil.html`;
    } else {
        window.alert(G_CODE_ERREURS[requete_connexion.code]);
    }
}