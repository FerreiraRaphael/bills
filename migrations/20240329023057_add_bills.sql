-- Create "bills" table
CREATE TABLE `bills` (
  `id` integer NULL,
  `name` text NOT NULL,
  `value` integer NOT NULL,
  `date` datetime NULL,
  `created_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `deleted_at` timestamp NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `datetime_chk` CHECK (
    "date" == strftime ('%Y-%m-%dT%H:%M:%SZ', "date")
    AND strftime ('%Y-%m-%dT%H:%M:%SZ', "date") IS NOT NULL
    AND "date" IS NOT NULL
  )
);
-- Create index "bills_name_value_date" to table: "bills"
CREATE UNIQUE INDEX `bills_name_value_date` ON `bills` (`name`, `value`, `date`);
-- Create trigger "updated_at_bills"
CREATE TRIGGER `updated_at_bills` AFTER UPDATE ON `bills` FOR EACH ROW BEGIN
UPDATE
  bills
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  id = NEW.id;
END;
