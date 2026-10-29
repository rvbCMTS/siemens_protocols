 SELECT
    DATETIME(ROUND(LastModification / 1000), 'unixepoch', 'localtime') as modified,
    HospitalName as hospital_name,
    HostIdentifier as host_identifier,
    (
        SELECT CAST(varvalue AS REAL)
        FROM GlobalVars
        WHERE name='DBVersion'
    ) AS db_version                                              
FROM GlobalData