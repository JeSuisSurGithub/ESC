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
                for (let i = 0; i < n_resultats; i++) {
                    tag_liste_resultats.innerHTML += `
                                <div class="card">
                                    <img src="/upload/${requete_recherche.val.nom_image[i]}" >
                                    <div class="texte">
                                        <p>
                                            Titre : ${requete_recherche.val.titre[i]} <br/>
                                            Genre: ${requete_recherche.val.genre[i]} <br/>
                                            Auteur: ${requete_recherche.val.auteur[i]} <br/>
                                            Editeur: ${requete_recherche.val.editeur[i]} <br/>
                                            Rayon: ${requete_recherche.val.rayon[i]} <br/>
                                            Date de Parution: ${requete_recherche.val.date_parution[i]} <br/>
                                            <br/>
                                        </p>
                                    </div>
                                </div>`;
                }
            }
        } else {
            window.alert(G_CODE_ERREURS[requete_recherche.code]);
        }
    });
}