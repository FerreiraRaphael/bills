-- Deploy bills:bills to sqlite
BEGIN;

DROP TABLE IF EXISTS bills;
CREATE TABLE "bills" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  "value" INTEGER NOT NULL,
  "date" DATETIME CONSTRAINT datetime_chk CHECK (
    "date" == strftime ('%Y-%m-%dT%H:%M:%SZ', "date")
    AND strftime ('%Y-%m-%dT%H:%M:%SZ', "date") IS NOT NULL
    AND "date" IS NOT NULL
  ),
  "main_tag_id" INTEGER,
  created_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at Timestamp,
  UNIQUE ("name", "value", "date"),
  PRIMARY KEY ("id" AUTOINCREMENT),
  FOREIGN KEY (main_tag_id) REFERENCES tags(id)
);

DROP TRIGGER IF EXISTS updated_at_bills;
CREATE TRIGGER updated_at_bills
AFTER
UPDATE
  ON bills FOR EACH ROW BEGIN
UPDATE
  bills
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  id = NEW.id;
END;

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
  bill_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  created_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at Timestamp,
  PRIMARY KEY ("bill_id", "tag_id"),
  FOREIGN KEY (bill_id) REFERENCES bills(id),
  FOREIGN KEY (tag_id) REFERENCES tags(id)
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
  bill_iD = NEW.bill_iD
  AND tag_id = NEW.tag_id;

END;

COMMIT;
