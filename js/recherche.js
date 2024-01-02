// Liste résultats recherche
const tag_liste_resultats = document.getElementById("liste_resultats")
if (parametre_get("entree") !== null) {
    const termes = decodeURIComponent(parametre_get("entree")).split(" ");
    api_recherche_livre(termes).then((requete_recherche) => {
        if (requete_recherche.code > 0) {
            const n_resultats = requete_recherche.val.titre.length;
            if (n_resultats === 0) {
                tag_liste_resultats.innerHTML = `
                            <div class="card">
                                <img src="/img/croix.png">
                                <div class="texte">
                                    <p>
                                        Aucun livre correspondant à la recherche
                                    </p>
                                </div>
                            </div>`
            } else {
                for (let i = 0; i < indices.length; i++) {
                    tag_liste_resultats.innerHTML += `
                                    <div class="card">
                                        <img src="/upload/${requete_recherche.val.nom_image[indices[i]]}" >
                                        <div class="texte">
                                            <p>
                                                Titre : ${requete_recherche.val.titre[indices[i]]} <br/>
                                                Genre: ${requete_recherche.val.genre[indices[i]]} <br/>
                                                Auteur: ${requete_recherche.val.auteur[indices[i]]} <br/>
                                                Editeur: ${requete_recherche.val.editeur[indices[i]]} <br/>
                                                Rayon: ${requete_recherche.val.rayon[indices[i]]} <br/>
                                                Date de Parution: ${requete_recherche.val.date_parution[indices[i]]} <br/>
                                                <br/>
                                            </p>
                                        </div>
                                    </div>`
                }
            }
        } else {
            window.alert(G_CODE_ERREURS[requete_recherche.code]);
        }
    });
}