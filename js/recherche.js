function recherche(entree, vtitre, vgenre, vauteur) {
    const termes = entree.split(" ");
    let vid = []

    boucle_ext: for (let i = 0; i < vtitre.length; i++) {
        let titre = vtitre[i];
        for (const terme of termes) {
            if (titre.toLowerCase().includes(terme.toLowerCase())) {
                vid.push(i);
                continue boucle_ext;
            }
        };

        let genre = vgenre[i];
        for (const terme of termes) {
            if (genre.toLowerCase().includes(terme.toLowerCase())) {
                vid.push(i);
                continue boucle_ext;
            }
        };

        let auteur = vauteur[i];
        for (const terme of termes) {
            if (auteur.toLowerCase().includes(terme.toLowerCase())) {
                vid.push(i);
                continue boucle_ext;
            }
        };
    }
    return vid;
}

// Liste résultats recherche
(async () => {
    const sortie = document.getElementById("liste_resultats")
    const livres = await api_livres();
    if (livres.code > 0) {
        const entree = decodeURIComponent(parametre_get("entree"));
        const indices = recherche(entree, livres.val.titre, livres.val.genre, livres.val.auteur);
        if (indices.length === 0) {
            sortie.innerHTML = `
                            <div class="card">
                                <img src="/img/croix.png">
                                <div class="texte">
                                    <p>
                                        Aucun livre correspondant à la recherche
                                    </p>
                                </div>
                            </div>`
        }
        for (let i = 0; i < indices.length; i++) {
            sortie.innerHTML += `
                            <div class="card">
                                <img src="/upload/${livres.val.nom_image[indices[i]]}" >
                                <div class="texte">
                                    <p>
                                        Titre : ${livres.val.titre[indices[i]]} <br/>
                                        Genre: ${livres.val.genre[indices[i]]} <br/>
                                        Auteur: ${livres.val.auteur[indices[i]]} <br/>
                                        Editeur: ${livres.val.editeur[indices[i]]} <br/>
                                        Rayon: ${livres.val.rayon[indices[i]]} <br/>
                                        Date de Parution: ${livres.val.date_parution[indices[i]]} <br/>
                                        <br/>
                                    </p>
                                </div>
                            </div>`
        }
    } else {
        window.alert(G_CODE_ERREURS[livres.code]);
    }
})();