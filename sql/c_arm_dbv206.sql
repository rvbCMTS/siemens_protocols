SELECT ApplicationGroup.name AS ApplicationGroup,
       ApplicationGroup.IsDefault AS ApplicationGroupIsDefault,
       ApplicationGroup_Application.OrderApplication,
       Application.name as Application,
       Application.Rotation,
       Application.EdgeEnhancementHigh,
       Application.EdgeEnhancementLow,
       Application.MotionDetectionHigh,
       Application.MotionDetectionLow,
       Application.ViewFlipX,
       Application.ViewFlipY,
       Application.MeasurementField,
       Application.Magnification,
       Application.AveragingLiveHigh,
       Application.AveragingLiveLow,
       Application.SpatialNoiseHigh,
       Application.SpatialNoiseLow,
       Application.SetBlack,
       Application.CenterShift,
       Application.SpotSize,
       Application.WidthFactor,
       Application.ZoomDoseFactor,
       AcquisitionModeConfig.Name as AcqusitionMode,
       AcquisitionModeConfig.AutoStore,
       AcquisitionModeConfig.StorageRate,
       AcquisitionModeConfig.MaxSceneLength,
       AcquisitionModeConfig.AutoLoop,
       AcquisitionModeConfig.NumFramesMask,
       AcquisitionModeConfig.AutoWindow,
       AcquisitionModeConfig.LIHStore,
       Triplet.name as Triplet,
       TripletElement.DoseOccurrence,
       TripletElement.Phase,
       TripletElement.FrameRate,
       TripletElement.DoseLevel,
       TripletElement.DoseRateIndex,
       TripletElement.NumImages,
       TripletElement.IsDefault AS TripletIsDefault,
       FluoroCurve.Name as FluoroCurve,
       FluoroCurve.IsHigh,
       NoiseSpatialFilterParameter.Name as NoiseSpatialFilterParameter,
       NoiseSpatialFilterParameter.Level,
       NoiseSpatialFilterParameter.Range,
       NoiseSpatialFilterParameter.LevelStd,
       NoiseTimeFilterParameter.Name as NoiseTimeFilterParameter,
       NoiseTimeFilterParameter.KMin,
       NoiseTimeFilterParameter.KMax,
       NoiseTimeFilterParameter.Threshold,
       NoiseTimeFilterParameter.MotionDetectionOn,
       SpatialFrequencyResponseParameter.Name as SpatialFrequencyResponseParameter,
       SpatialFrequencyResponseParameter.EdgeFilterGain,
       SpatialFrequencyResponseParameter.EdgeFilterKernel,
       SpatialFrequencyResponseParameter.HarmonisationGain,
       SpatialFrequencyResponseParameter.HarmonisationKernel,
       OrbitalScanConfig.Name as OrbitalScanConfig,
       AngularScanConfig.Name as AngularScanConfig,
       BasicRecoSet.Name AS BasicRecoSet
from Application

JOIN ApplicationGroup_Application ON ApplicationGroup_Application.ID_Application=Application.ID
JOIN ApplicationGroup ON ApplicationGroup.ID=ApplicationGroup_Application.ID_ApplicationGroup
JOIN AcquisitionModeConfig on Application.ID_AcqModeConfigFluoro=AcquisitionModeConfig.ID
JOIN Triplet on AcquisitionModeConfig.ID_Triplet=Triplet.ID
JOIN TripletElement on TripletElement.ID_Triplet=Triplet.ID
JOIN FluoroCurve on TripletElement.ID_FluoroCurve=FluoroCurve.ID
JOIN NoiseSpatialFilterParameter on TripletElement.ID_NoiseSpatialFilterParameter=NoiseSpatialFilterParameter.ID
JOIN NoiseTimeFilterParameter on TripletElement.ID_NoiseTimeFilterParameter=NoiseTimeFilterParameter.ID
JOIN SpatialFrequencyResponseParameter on TripletElement.ID_SpatialFrequencyResponseParameter=SpatialFrequencyResponseParameter.ID
LEFT JOIN OrbitalScanConfig on TripletElement.ID_OrbitalScanConfig=OrbitalScanConfig.ID
LEFT JOIN AngularScanConfig on TripletElement.ID_AngularScanConfig=AngularScanConfig.ID
LEFT JOIN BasicRecoSet on TripletElement.ID_BasicRecoSet=BasicRecoSet.ID
