DROP VIEW IF EXISTS ExposureParameter;
CREATE VIEW ExposureParameter AS

WITH
Exposure_Parameter AS (
    SELECT
		OGP.ID as ID_OGP,
		OGP.Name as ris_name,
		Technique.Value AS technique,
        CAST(OGP_kV.Value  AS REAL) / 10   AS kv,
        CAST(RADOGP_mAs.Value AS REAL) / 100  AS mas,
        CAST(RADOGP_ms.Value  AS REAL) / 10   AS ms,
		FilterType.Name AS filter_cu,
		Focus.Name AS focus,
		OGP.Grid as grid,
		Dose_RAD.Dose AS aec_dose_level,
		SDMDominant.Name AS aec_dominant,
		RAD_OGP.ExposureCorrection AS aec_exposure_correction
		
    FROM OGP
	JOIN RAD_OGP ON RAD_OGP.ID = OGP.ID
    JOIN OGP_kV  ON OGP.ID_kV = OGP_kV.ID 
    LEFT JOIN RADOGP_mAs ON RADOGP_mAs.ID = RAD_OGP.ID_mAs
    LEFT JOIN RADOGP_ms  ON RADOGP_ms.ID  = RAD_OGP.ID_ms
	JOIN Technique ON RAD_OGP.Id_technique = Technique.Id
	JOIN Dose_RAD ON RAD_OGP.ID_dose = Dose_RAD.Id
	JOIN Focus ON OGP.Id_focus = Focus.Id
	JOIN FilterType ON OGP.Id_filtertype = FilterType.Id
	LEFT JOIN SDMDominant ON OGP.ID_SDMDominant = SDMDominant.Id
)

SELECT * FROM Exposure_Parameter
		