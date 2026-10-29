DROP VIEW IF EXISTS SpatialFreqency;

CREATE VIEW SpatialFreqency AS

WITH
spatial_frequency AS (
WITH SpatialFrequencyUnion AS (
    SELECT ID_ImaSpatialFreqParam
    FROM OGP
	JOIN Exam_OGPExtended ON
		OGP.Id = Exam_OGPExtended.Id_ogp
	JOIN Exam ON
		Exam.Id = Exam_OGPExtended.Id_exam
		AND Exam.status=2

    UNION

    SELECT ID_ImaSpatialFreqParam
    FROM FluoroProgram
)
	
	SELECT DISTINCT
		SpatialFrequencyParameter.Name AS name,
		DiamondViewID.Name AS diamond_view,
		EdgeFilterKernel.Value AS edge_filter_kernel_size,
		ROUND(SpatialFrequencyParameter.Edgefiltergain, 2) AS edge_filter_gain,
		HarmonisKernel.Value AS harmonization_kernel_size,
		ROUND(SpatialFrequencyParameter.HarmonisGain, 2) AS harmonization_gain,
		SpatialFrequencyParameter.Noisereduction AS noise_reduction

	FROM SpatialFrequencyParameter
	
	JOIN EdgeFilterKernel ON
		SpatialFrequencyParameter.Id_edgefilterkernel = EdgeFilterKernel.Id
	JOIN HarmonisKernel ON
		SpatialFrequencyParameter.Id_harmoniskernel = HarmonisKernel.Id
	JOIN DiamondViewID ON
		SpatialFrequencyParameter.ID_DiamondViewID = DiamondViewID.ID
	JOIN SpatialFrequencyUnion ON
		SpatialFrequencyUnion.ID_ImaSpatialFreqParam = SpatialFrequencyParameter.ID
)

SELECT * FROM spatial_frequency
ORDER BY spatial_frequency.name
