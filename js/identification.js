async function identifier() {
    const tag_compteur = document.getElementById("compteur");
    let temps_limite = 10;
    let intervalle = setInterval(() => {
        tag_compteur.innerHTML
            = `Veuillez scanner la carte à identifier (il vous reste ${--temps_limite}s)`;
        if (temps_limite == 0) {
            clearInterval(intervalle);
            tag_compteur.innerHTML = "Temps écoulé, veuillez réinitier la procédure";
        }
    }, 1000);

    const res = await api_uid_nfc();
    clearInterval(intervalle);
    if (res.code > 0) {
        const requete_livre = await api_livres();
        if (requete_livre.code > 0) {
            const index = requete_livre.val.uid_nfc.indexOf(res.val);
            if (index !== -1) {
                const res_hist = await api_info_livre(res.val);
                if (res_hist.code > 0) {
                    const sortie = document.getElementById("res_ident");
                    // Si n'a jamais été emprunté ou emprunté mais rendu
                    const disponible = (res_hist.val.rendu === null)|| (res_hist.val.rendu === true);
                    sortie.innerHTML = `
                        <div class="card">
                            <img src="/upload/${requete_livre.val.nom_image[index]}">
                            <div class="texte">
                                <p>
                                    Titre: ${requete_livre.val.titre[index]}<br/>
                                    Genre: ${requete_livre.val.genre[index]}<br/>
                                    Auteur: ${requete_livre.val.auteur[index]}<br/>
                                    Editeur: ${requete_livre.val.editeur[index]}<br/>
                                    Rayon: ${requete_livre.val.rayon[index]}<br/>
                                    Date de Parution: ${requete_livre.val.date_parution[index]}<br/>
                                    Disponibilité: ${disponible}
                                </p>
                            </div>
                        </div>`;
                } else {
                    window.alert(G_CODE_ERREURS[res_hist.code]);
                }
            } else {
                window.alert("Carte de livre inconnue");
            }
        } else {
            window.alert(G_CODE_ERREURS[requete_livre.code])
        }
    } else {
        window.alert(G_CODE_ERREURS[res.code])
    }
}