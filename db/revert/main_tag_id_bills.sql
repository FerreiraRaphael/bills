-- Revert bills:main_tag_id_bills from sqlite
PRAGMA foreign_keys = off;

BEGIN;

ALTER TABLE
  bills RENAME TO bills_old;

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

INSERT INTO
  bills SELECT
      "id",
      "name",
      "value",
      "date",
      "created_at",
      "updated_at",
      "deleted_at"
    FROM
      bills_old;

DROP TABLE "bills_old";

ALTER TABLE bills RENAME to bills_old;
ALTER TABLE bills_old RENAME to bills;

COMMIT;

PRAGMA foreign_keys = on;
