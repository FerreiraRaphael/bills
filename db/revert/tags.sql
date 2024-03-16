-- Revert bills:tags from sqlite
BEGIN;

DROP TABLE "tags";

DROP TABLE "bills_tags";

COMMIT;
