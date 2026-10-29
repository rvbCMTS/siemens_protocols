DROP VIEW IF EXISTS Exam_OGPExtended;

CREATE VIEW Exam_OGPExtended AS
WITH
-- all Ortho OGPs
Ortho_OGP AS (
    SELECT o.ID
    FROM OGP o
    JOIN OperationMode om ON o.ID_OperationMode = om.ID
    WHERE om.Name = 'Ortho'
),

-- existing exams for Ortho OGPs
Ortho_OGP_Exam AS (
    SELECT e.id_ogp, e.id_exam
    FROM Exam_OGP e
    JOIN Ortho_OGP o ON o.ID = e.id_ogp
),

-- derive exam for every Ortho OGP (carry-forward)
Virtual_Ortho_Exam AS (
    SELECT
        o.ID AS id_ogp,
        COALESCE(
            e.id_exam,
            (
                SELECT e2.id_exam
                FROM Ortho_OGP_Exam e2
                WHERE e2.id_ogp < o.ID
                ORDER BY e2.id_ogp DESC
                LIMIT 1
            )
        ) AS id_exam
    FROM Ortho_OGP o
    LEFT JOIN Ortho_OGP_Exam e
        ON e.id_ogp = o.ID
),

-- derive exam for alternative OGP (fallback to original OGP)
Alternative_Exam_Fallback AS (
    SELECT
        a.id_alternativeogp AS id_ogp,
        COALESCE(eo_alt.id_exam, eo_orig.id_exam) AS id_exam
    FROM AlternativeOGP a
    JOIN OGP oa
        ON a.id_alternativeogp = oa.ID
    LEFT JOIN Exam_OGP eo_alt
        ON eo_alt.id_ogp = oa.ID
    JOIN OGP o_orig
        ON a.id_ogp = o_orig.ID
    LEFT JOIN Exam_OGP eo_orig
        ON eo_orig.id_ogp = o_orig.ID
),

-- real OGPs with existing exams
Real_OGP AS (
    SELECT DISTINCT id_ogp FROM Exam_OGP
),

-- final extended table
Exam_OGP_Extended AS (
    -- real rows
    SELECT id_ogp, id_exam
    FROM Exam_OGP

    UNION ALL

    -- virtual Ortho rows
    SELECT v.id_ogp, v.id_exam
    FROM Virtual_Ortho_Exam v
    LEFT JOIN Real_OGP r ON r.id_ogp = v.id_ogp
    WHERE r.id_ogp IS NULL

    UNION ALL

    -- virtual Alternative fallback rows
    SELECT a.id_ogp, a.id_exam
    FROM Alternative_Exam_Fallback a
    LEFT JOIN Real_OGP r ON r.id_ogp = a.id_ogp
    WHERE r.id_ogp IS NULL
)

SELECT
    id_ogp,
    id_exam
FROM Exam_OGP_Extended

