DROP VIEW IF EXISTS FluoroSetting;

CREATE VIEW FluoroSetting AS

WITH

fluoro_setting AS(
	SELECT DISTINCT
		FPSet.Name AS fluoro_program,
		FluoroProgram.FluoroMode AS fluoro_mode,
		FrameRate.Value AS frame_rate,
		ROUND(FluoroProgram.DoseRateIndex, 2) AS dose_rate_index,
		FluoroCurve.Name AS fluoro_curve,
		FilterType.Name AS filter_type,
		NoiseReduction.Value AS noise_reduction,
		DoseLevel_FP.Value AS detector_dose_level,
		SpatialFrequencyParameter.Name AS spatial_frequency_parameter

	FROM FluoroProgram

	JOIN FPSet ON
		FluoroProgram.ID_FPSet = FPSet.Id
	JOIN FrameRate ON
		FluoroProgram.ID_FrameRate = FrameRate.Id
	JOIN FluoroCurve ON
		FluoroProgram.ID_FluoroCurve = FluoroCurve.ID
	JOIN FilterType ON
		FluoroProgram.ID_FilterType = FilterType.ID
	JOIN NoiseReduction ON
		FluoroProgram.ID_NoiseReduction = NoiseReduction.ID
	JOIN DoseLevel_FP ON
		FluoroProgram.ID_DoseLevel = DoseLevel_FP.ID
	JOIN SpatialFrequencyParameter ON
		FluoroProgram.ID_ImaSpatialFreqParam = SpatialFrequencyParameter.ID
	JOIN OGP ON
		OGP.ID_FPSet = FPSet.ID
	JOIN Exam_OGPExtended ON
		OGP.Id = Exam_OGPExtended.Id_ogp
	JOIN Exam ON
		Exam.Id = Exam_OGPExtended.Id_exam
		AND Exam.status=2
)

SELECT * FROM fluoro_setting