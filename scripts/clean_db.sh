pushd .
  sqlite3 db/"$@".sqlite < db/clean_db.sql
popd

