-- Disable the enforcement of foreign-keys constraints
PRAGMA foreign_keys = off;
-- Create "new_bills" table
CREATE TABLE `new_bills` (
  `id` integer NULL,
  `name` text NOT NULL,
  `value` integer NOT NULL,
  `date` datetime NULL,
  `main_tag_id` integer NULL,
  `created_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `deleted_at` timestamp NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `0` FOREIGN KEY (`main_tag_id`) REFERENCES `tags` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT `datetime_chk` CHECK (
    "date" == strftime ('%Y-%m-%dT%H:%M:%SZ', "date")
    AND strftime ('%Y-%m-%dT%H:%M:%SZ', "date") IS NOT NULL
    AND "date" IS NOT NULL
  )
);
-- Copy rows from old table "bills" to new temporary table "new_bills"
INSERT INTO `new_bills` (`id`, `name`, `value`, `date`, `created_at`, `updated_at`, `deleted_at`) SELECT `id`, `name`, `value`, `date`, `created_at`, `updated_at`, `deleted_at` FROM `bills`;
-- Drop "bills" table after copying rows
DROP TABLE `bills`;
-- Rename temporary table "new_bills" to "bills"
ALTER TABLE `new_bills` RENAME TO `bills`;
-- Create index "bills_name_value_date" to table: "bills"
CREATE UNIQUE INDEX `bills_name_value_date` ON `bills` (`name`, `value`, `date`);
-- Enable back the enforcement of foreign-keys constraints
PRAGMA foreign_keys = on;
