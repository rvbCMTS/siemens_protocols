SELECT
	OGP.Name AS ris_name,
	Exam.name as exam_name,
	BodyPart.Name AS body_part,
	ExposureParameter.technique,
	ExposureParameter.kv,
	ExposureParameter.mas,
	ExposureParameter.ms,
	ExposureParameter.filter_cu,
	ExposureParameter.focus,
	ExposureParameter.grid,
	ExposureParameter.aec_dose_level,
	ExposureParameter.aec_exposure_correction,
	ExposureParameter.aec_dominant,
	PostProcessing.spatial_frequency_parameter,
	PostProcessing.lut,
	PostProcessing.image_auto_amplification,
	PostProcessing.image_amplification_gain,
	WindowSetting.image_win_auto_windowing,
	WindowSetting.image_win_center,
	WindowSetting.image_win_center_shift,
	WindowSetting.image_win_width,
	WindowSetting.image_win_width_factor,
	WindowSetting.bandwidth,
	OperationMode.Name as operation_mode,
	RAD_OGP.OGP_NumInSet AS ortho_number,	
	FPSet.Name AS fluoro_program,
	StandPosition.Name AS stand_position,
	RAD_OGP.StandShutter1 AS shutter_1,
	RAD_OGP.StandShutter2 AS shutter_2,
	AcquisitionSystem.Name AS acquisition_system,
	EXI_Parameter.Name AS exi_name,
	EXI_Parameter.TargetEXI as exi_target
FROM OGP

JOIN Exam_OGPExtended ON
	OGP.Id = Exam_OGPExtended.Id_ogp
JOIN Exam ON
	Exam.Id = Exam_OGPExtended.Id_exam AND
	Exam.status=2
JOIN BodyPart ON
	BodyPart.Id = OGP.Id_bodypart
JOIN AcquisitionSystem ON
	AcquisitionSystem.Id = OGP.Id_acqsystem
JOIN RAD_OGP ON
	RAD_OGP.ID = OGP.ID
LEFT JOIN ExposureParameter ON
	ExposureParameter.id_ogp = OGP.ID
LEFT JOIN WindowSetting ON
	WindowSetting.ID_OGP = OGP.ID
LEFT JOIN PostProcessing ON
	PostProcessing.ID_OGP = OGP.ID
LEFT JOIN FPSet ON
	FPset.ID = OGP.ID_FPSet
LEFT JOIN EXI_Parameter ON
	RAD_OGP.ID_EXI_Parameter = EXI_Parameter.Id
LEFT JOIN StandPosition ON
	OGP.ID_StandPosition = StandPosition.ID
JOIN OperationMode ON
	OGP.ID_OperationMode = OperationMode.ID

WHERE
OGP.Name NOT LIKE '-%' AND
OGP.Name NOT LIKE '. _%' AND
OGP.Name NOT LIKE '%\_%' ESCAPE '\'

ORDER BY exam_name, ris_name ;