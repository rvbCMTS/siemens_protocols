SELECT 	OGP.Name AS ris_name,
        CASE
            WHEN Exam.name IS NOT NULL THEN Exam.Name
            ELSE Exam2.name
        END AS exam_name,
		BodyPart.Name AS body_part,
		AcquisitionSystem.Name AS acquisition_system,
		Technique.Value AS technique,
		CAST(OGP_kV.Value AS float)/10 AS kv,
		CAST(RADOGP_mAs.Value AS float)/100 AS mas,
		FilterType.Name AS filter_cu,
		Focus.Name AS focus,
		OGP.Grid AS grid,
		DiamondViewID.Name AS diamond_view,
		EdgeFilterKernel.Value AS edge_filter_kernel_size,
		SpatialFrequencyParameter.Edgefiltergain AS edge_filter_gain,
		HarmonisKernel.Value AS harmonization_kernel_size,
		SpatialFrequencyParameter.Harmonisgain AS harmonization_gain,
		SpatialFrequencyParameter.Noisereduction AS noise_reduction,
		RAD_OGP.Imageautoamplification AS image_auto_amplification,
		RAD_OGP.ImageAmplification AS image_amplification_gain,
		Dose_RAD.Sensitivity AS sensitivity,
		GradationParameter.Name AS lut,
		FPSet.Name AS fp_set,
        EXI_Parameter.Name AS exi_name,
        EXI_Parameter.TargetEXI as exi_target
FROM OGP


LEFT OUTER JOIN Exam_OGP ON OGP.Id = Exam_OGP.Id_ogp
LEFT OUTER JOIN Exam ON Exam.Id = Exam_OGP.Id_exam
LEFT OUTER JOIN AlternativeOGP on OGP.ID = AlternativeOGP.id_alternativeogp
LEFT OUTER JOIN Exam_OGP AS eogp ON AlternativeOGP.ID_OGP = eogp.id_ogp
LEFT OUTER JOIN Exam AS Exam2 ON eogp.id_exam = Exam2.id
INNER JOIN BodyPart ON BodyPart.Id = OGP.Id_bodypart
INNER JOIN AcquisitionSystem ON AcquisitionSystem.Id = OGP.Id_acqsystem
INNER JOIN OGP_kV  ON OGP_kV.ID = OGP.ID_kV
INNER JOIN RAD_OGP ON RAD_OGP.ID = OGP.ID
LEFT OUTER JOIN RADOGP_mAs ON RAD_OGP.Id_mas = RADOGP_mAs.Id
INNER JOIN Technique ON RAD_OGP.Id_technique = Technique.Id
INNER JOIN FilterType ON OGP.Id_filtertype = FilterType.Id
INNER JOIN Focus ON OGP.Id_focus = Focus.Id
INNER JOIN SpatialFrequencyParameter ON OGP.Id_imaspatialfreqparam = SpatialFrequencyParameter.Id
INNER JOIN DiamondViewID ON SpatialFrequencyParameter.Id_diamondviewid = DiamondViewID.Id
INNER JOIN EdgeFilterKernel ON SpatialFrequencyParameter.Id_edgefilterkernel = EdgeFilterKernel.Id
INNER JOIN HarmonisKernel ON SpatialFrequencyParameter.Id_harmoniskernel = HarmonisKernel.Id
INNER JOIN Dose_RAD ON RAD_OGP.Id_dose = Dose_RAD.Id
INNER JOIN GradationParameter ON RAD_OGP.Id_imagegradation = GradationParameter.Ids
LEFT OUTER JOIN FPSet ON FPset.ID = OGP.ID_FPSet
INNER JOIN EXI_Parameter on RAD_OGP.ID_EXI_Parameter = EXI_Parameter.Id


WHERE
OGP.status=2
AND OGP.Type='SIEMENSDEFAULT'
AND ris_name NOT LIKE '-%'
AND ris_name NOT LIKE '. _%'
AND ris_name NOT LIKE '%\_%' ESCAPE '\'
AND Exam_name NOT NULL

ORDER BY exam_name ;