-- Verify bills:main_tag_id_bills on sqlite

BEGIN;

SELECT * FROM bills JOIN tags on tags.id == bills.main_tag_id;

ROLLBACK;
