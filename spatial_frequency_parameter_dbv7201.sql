SELECT 	SpatialFrequencyParameter.Name AS name,
		DiamondViewID.Name AS diamond_view,
		EdgeFilterKernel.Value AS edge_filter_kernel_size,
		ROUND(SpatialFrequencyParameter.Edgefiltergain, 2) AS edge_filter_gain,
		HarmonisKernel.Value AS harmonization_kernel_size,
		ROUND(SpatialFrequencyParameter.HarmonisGain, 2) AS harmonization_gain,
		SpatialFrequencyParameter.Noisereduction AS noise_reduction

FROM SpatialFrequencyParameter

INNER JOIN EdgeFilterKernel ON SpatialFrequencyParameter.Id_edgefilterkernel = EdgeFilterKernel.Id
INNER JOIN HarmonisKernel ON SpatialFrequencyParameter.Id_harmoniskernel = HarmonisKernel.Id
INNER JOIN DiamondViewID ON SpatialFrequencyParameter.ID_DiamondViewID = DiamondViewID.ID


WHERE
SpatialFrequencyParameter.Identifier LIKE 'c%'

ORDER BY SpatialFrequencyParameter.name ;