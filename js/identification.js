async function identifier() {
    const tag_compteur = document.getElementById("compteur");
    const tag_res_ident = document.getElementById("res_ident");

    let temps_limite = 10;
    let intervalle = setInterval(() => {
        tag_compteur.innerHTML
            = `Veuillez scanner la carte à identifier (il vous reste ${--temps_limite}s)`;
        if (temps_limite == 0) {
            clearInterval(intervalle);
            tag_compteur.innerHTML = "Temps écoulé, veuillez réinitier la procédure";
        }
    }, 1000);

    const requete_uid = await api_uid_nfc();
    clearInterval(intervalle);
    if (requete_uid.code > 0) {
        const requete_livre = await api_info_livre(requete_uid.val);
        if (requete_livre.code > 0) {
            if (requete_livre.val.id !== null) {
                const requete_emprunt = await api_info_emprunt(requete_uid.val);
                if (requete_emprunt.code > 0) {
                    const disponible = (res_hist.val.disponible === null)|| (res_hist.val.disponible === true);
                    tag_res_ident.innerHTML = `
                            <div class="card">
                                <img src="/upload/${requete_livre.val.nom_image}">
                                <div class="texte">
                                    <p>
                                        Titre: ${requete_livre.val.titre}<br/>
                                        Genre: ${requete_livre.val.genre}<br/>
                                        Auteur: ${requete_livre.val.auteur}<br/>
                                        Editeur: ${requete_livre.val.editeur}<br/>
                                        Rayon: ${requete_livre.val.rayon}<br/>
                                        Date de Parution: ${requete_livre.val.date_parution}<br/>
                                        Disponibilité: ${disponible}
                                    </p>
                                </div>
                            </div>`;
                } else {
                    window.alert(G_CODE_ERREURS[requete_emprunt.code])
                }
            } else {
                window.alert("Carte de livre inconnue");
            }
        } else {
            window.alert(G_CODE_ERREURS[requete_livre.code])
        }
    } else {
        window.alert(G_CODE_ERREURS[requete_uid.code])
    }
}