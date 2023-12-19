#/bin/sh
sqlite3 "esc.db" ".read init.sql"
sqlite3 "esc.db" ".read donnees_test.sql"