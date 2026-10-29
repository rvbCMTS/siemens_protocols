SELECT EXISTS (
    SELECT 1
    FROM sqlite_master
    WHERE type = 'table'
      AND name = 'Triplet'
) AS triplet_table_exists