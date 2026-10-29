DROP VIEW IF EXISTS PostProcessing;

CREATE VIEW PostProcessing AS
WITH
Post_Processing AS (
	SELECT
		OGP.ID as ID_OGP,
		OGP.name as ris_name,
		SpatialFrequencyParameter.Name AS spatial_frequency_parameter,
		GradationParameter.Name AS lut,
		RAD_OGP.Imageautoamplification AS image_auto_amplification,
		ROUND(RAD_OGP.ImageAmplification, 2) AS image_amplification_gain
	FROM OGP
	JOIN SpatialFrequencyParameter ON
		OGP.Id_imaspatialfreqparam = SpatialFrequencyParameter.Id
	JOIN RAD_OGP ON
		RAD_OGP.ID = OGP.ID
	JOIN GradationParameter
		ON RAD_OGP.Id_imagegradation = GradationParameter.Ids
)

SELECT * FROM Post_Processing