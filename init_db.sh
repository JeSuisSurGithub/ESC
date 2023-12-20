#/bin/sh
sqlite3 "esc.db" ".read init.sql"
sqlite3 "esc.db" ".read donnees_test.sql"
./admin.py user1@mail.net 11111 jean pierre 2000-01-01 0