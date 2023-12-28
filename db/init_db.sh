#/bin/sh
rm esc.sqlite
sqlite3 "esc.sqlite" ".read init.sql"
./ajout_compte.py user1@mail.net 11111 lemprunteur 2000-01-01 1
./ajout_compte.py admin1@mail.net 11111 admin1 2000-01-01 0