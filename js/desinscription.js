async function desinscription() {
    const tag_email = document.getElementById("email");
    const tag_motdepasse = document.getElementById("motdepasse");

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

    const res = await api_desinscription(tag_email.value, tag_motdepasse.value);
    if (res.code > 0) {
        window.location.href = window.location.origin;
    } else {
        window.alert(G_CODE_ERREURS[res.code]);
    }
}