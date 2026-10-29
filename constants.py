PARAMETERS_FOR_COMPARISON = "parameters_for_comparison"
PARAMETER_LIST = "parameter_list"
SHEET_NAME = "sheet_name"
GROUP_BY_COLUMN = "group_by_column"


PEX = {
    PARAMETERS_FOR_COMPARISON:{
        PARAMETER_LIST:(["stand_position", "body_part", "acquisition_system", "technique",  "kv", "mas", "ms", "aec_dose_level", "aec_dominant",
                                  "aec_exposure_correction", "spatial_frequency_parameter","filter_cu", "focus", "grid", "shutter_1", "shutter_2",
                                   "image_auto_amplification", "image_amplification_gain", "image_win_auto_windowing", "lut", "fluoro_program", "exi_name", "exi_target"]),
        GROUP_BY_COLUMN: "ris_name"
    },
    SHEET_NAME: "Pex",

}

SPM ={
    PARAMETERS_FOR_COMPARISON: {
        PARAMETER_LIST: ["diamond_view", "edge_filter_kernel_size", "edge_filter_gain", "harmonization_kernel_size", "harmonization_gain", "noise_reduction"],
        GROUP_BY_COLUMN: "name"
    },
    SHEET_NAME: "SpatialFrequencyParameter",  
}

FLUORO ={
    PARAMETERS_FOR_COMPARISON: {
        PARAMETER_LIST: ["frame_rate", "dose_rate_index", "fluoro_curve", "filter_type", "noise_reduction", "detector_dose_level", "spatial_frequency_parameter"],
        GROUP_BY_COLUMN: ["fluoro_program", "fluoro_mode"]
    },
    SHEET_NAME: "FluoroProgram"
}