-- Verify bills:tags on sqlite
BEGIN;

SELECT
  *
FROM
  bills AS b
  JOIN bills_tags AS bt ON bt.bill_id = = b.id
  JOIN tags AS t ON bt.tag_id = = t.id;

ROLLBACK;
