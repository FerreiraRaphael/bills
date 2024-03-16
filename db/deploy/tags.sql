-- Deploy bills:tags to sqlite
BEGIN;

CREATE TABLE "tags" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  created_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at Timestamp,
  UNIQUE ("name"),
  PRIMARY KEY ("id" AUTOINCREMENT)
);

CREATE TABLE "bills_tags" (
  bill_iD INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  created_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at Timestamp,
  PRIMARY KEY ("bill_id", "tag_id"),
  FOREIGN KEY (bill_id) REFERENCES bills (id),
  FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TRIGGER updated_at_tags
AFTER
UPDATE
  ON tags FOR EACH ROW BEGIN
UPDATE
  tags
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  id = NEW.id;

END;

CREATE TRIGGER updated_at_bills_tags
AFTER
UPDATE
  ON bills_tags FOR EACH ROW BEGIN
UPDATE
  bills_tags
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  id = NEW.id;

END;

COMMIT;
