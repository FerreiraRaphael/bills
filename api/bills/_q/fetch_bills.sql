WITH q_bills AS (
  SELECT
    *
  FROM
    bills AS b
  WHERE
    b.deleted_at IS NULL
)
SELECT
  q_bills.*
  {% if join_main_tag +%}
  ,(
    SELECT
      json_object( {{ render_tag("tags") | sqlsafe }} )
    FROM
      tags
    WHERE
      id = q_bills.main_tag_id
      AND tags.deleted_at IS NULL
  ) AS main_tag
  {% endif %}
  {% if join_tags +%}
  ,(
    SELECT
      json_group_array(json_object( {{ render_tag("tags") | sqlsafe }} ))
    FROM
      tags
      INNER JOIN bills_tags AS bt on bt.bill_id = q_bills.id
      AND bt.tag_id = tags.id
    WHERE
      tags.deleted_at IS NULL
  ) AS tags
  {% endif %}
FROM
  q_bills;
