-- Revert bills:bills from sqlite
BEGIN;

DROP TABLE bills;

COMMIT;
