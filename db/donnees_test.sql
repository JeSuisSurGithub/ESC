INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc)
    VALUES ('les fleurs du mal', 'poésie', '27A', '1999-01-01', '5E1CF2C777');

INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc)
    VALUES ('livre2', 'roman', '2B', '1800-12-12', '00-0001-00');

INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc)
    VALUES ('livre3', 'politique', '1A', '1850-06-06', '00-0009-00');

INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc)
    VALUES ('livre4', 'roman', '2C', '1750-06-06', '00-1111-00');

INSERT INTO LIVRE (titre, genre, rayon, date_parution, guid_nfc)
    VALUES ('livre5', 'roman', '2E', '1650-03-06', '00-55AA-00');

INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
    VALUES ('1', '1', '2023-11-24', '2023-12-01', 0);

INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
    VALUES ('1', '3', '2023-12-01', '2023-12-12', 1);

INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
    VALUES ('1', '4', '2023-12-15', '2023-12-24', 0);

INSERT INTO EMPRUNT (id_u, id_l, date_debut, date_fin, rendu)
    VALUES ('1', '5', '2023-12-18', '2023-12-20', 0);