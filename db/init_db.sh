#/bin/sh
rm esc.db
sqlite3 "esc.db" ".read init.sql"
sqlite3 "esc.db" ".read donnees_test.sql"
./admin.py user1@mail.net 11111 lemprunteur93 2000-01-01 1
./admin.py admin1@mail.net 11111 admin1 2000-01-01 0