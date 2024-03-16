-- Deploy bills:main_tag_id_bills to sqlite

PRAGMA foreign_keys=off;

BEGIN;

ALTER TABLE bills RENAME TO bills_old;

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

INSERT INTO bills SELECT *, NULL as main_tag_id FROM bills_old;

DROP TABLE "bills_old";

ALTER TABLE bills RENAME to bills_old;
ALTER TABLE bills_old RENAME to bills;

COMMIT;

PRAGMA foreign_keys=on;
