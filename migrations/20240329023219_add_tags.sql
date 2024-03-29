-- Create "tags" table
CREATE TABLE `tags` (
  `id` integer NULL,
  `name` text NOT NULL,
  `created_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `deleted_at` timestamp NULL,
  PRIMARY KEY (`id`)
);
-- Create index "tags_name" to table: "tags"
CREATE UNIQUE INDEX `tags_name` ON `tags` (`name`);
-- Create trigger "updated_at_tags"
CREATE TRIGGER `updated_at_tags` AFTER UPDATE ON `tags` FOR EACH ROW BEGIN
UPDATE
  tags
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  id = NEW.id;

END;
-- Create "bills_tags" table
CREATE TABLE `bills_tags` (
  `bill_id` integer NOT NULL,
  `tag_id` integer NOT NULL,
  `created_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NULL DEFAULT (CURRENT_TIMESTAMP),
  `deleted_at` timestamp NULL,
  PRIMARY KEY (`bill_id`, `tag_id`),
  CONSTRAINT `0` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT `1` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create trigger "updated_at_bills_tags"
CREATE TRIGGER `updated_at_bills_tags` AFTER UPDATE ON `bills_tags` FOR EACH ROW BEGIN
UPDATE
  bills_tags
SET
  updated_at = CURRENT_TIMESTAMP
WHERE
  bill_iD = NEW.bill_iD
  AND tag_id = NEW.tag_id;

END;
