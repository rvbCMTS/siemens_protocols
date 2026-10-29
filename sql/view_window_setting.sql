DROP VIEW IF EXISTS WindowSetting;

CREATE VIEW WindowSetting AS

WITH
Window_Setting AS (
	SELECT
		OGP.ID AS ID_OGP,
		OGP.name AS ris_name,
		RAD_OGP.ImageWinAutowindowing AS image_win_auto_windowing,
		RAD_OGP.ImageWinCenter AS image_win_center,
		RAD_OGP.ImageWinCenterShift AS image_win_center_shift,
		RAD_OGP.ImageWinWidth AS image_win_width,
		RAD_OGP.ImageWinWidthFactor AS image_win_width_factor,
		OGP.Bandwidth AS bandwidth
	FROM OGP
	JOIN RAD_OGP ON
		RAD_OGP.ID = OGP.ID
)

SELECT * FROM Window_Setting
