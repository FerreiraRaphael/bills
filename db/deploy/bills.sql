-- Deploy bills:bills to sqlite
BEGIN;

CREATE TABLE "bills" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  "value" INTEGER NOT NULL,
  "date" DATETIME CONSTRAINT datetime_chk CHECK (
    "date" == strftime ('%Y-%m-%dT%H:%M:%SZ', "date")
    AND strftime ('%Y-%m-%dT%H:%M:%SZ', "date") IS NOT NULL
    AND "date" IS NOT NULL
  ),
  created_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at Timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at Timestamp,
  UNIQUE ("name", "value", "date"),
  PRIMARY KEY ("id" AUTOINCREMENT)
);

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

COMMIT;
