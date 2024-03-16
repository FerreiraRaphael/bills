-- Verify bills:bills on sqlite
BEGIN;

SELECT
  *
FROM
  "bills";

ROLLBACK;
