import sqlite3
import pandas
from pathlib import Path

def _concat_ris_name_for_ortho_organ_program(df: pandas.DataFrame) -> pandas.DataFrame:
    orto_ogp = df["ortho_number"] != 0
    df.loc[orto_ogp, "ris_name"] = (df.loc[orto_ogp, "ris_name"].astype(str)
                                    + " #"
                                    + df.loc[orto_ogp, "ortho_number"].astype(str)
    )
    return df

def parse_db(path_to_db: Path, db_version: float, modified: str, hospital_name: str, host_identifier: str) -> tuple[pandas.DataFrame, pandas.DataFrame, pandas.DataFrame]:

    with sqlite3.connect(path_to_db) as conn:

        cur = conn.cursor()

        # create views
        cur.executescript(Path("sql\\view_exam_ogp_extended.sql").read_text())
        cur.executescript(Path("sql\\view_post_processing.sql").read_text())
        cur.executescript(Path("sql\\view_window_setting.sql").read_text())
        cur.executescript(Path("sql\\view_spatial_frequency_parameter.sql").read_text())
        cur.executescript(Path("sql\\view_fluoro_setting.sql").read_text())

        if 70 < db_version <= 72.02:
            cur.executescript(Path("sql\\view_exposure_parameter_dbv7202.sql").read_text())
        elif 72.03 <= db_version:
            cur.executescript(Path("sql\\view_exposure_parameter.sql").read_text())
        
        conn.commit()

        # fetch organ programs
        df = pandas.read_sql_query(Path('sql\\query_organ_programs.sql').read_text(), conn)
        df = _concat_ris_name_for_ortho_organ_program(df)
        
        # fetch spatial frequency parameters
        sfp = pandas.read_sql_query(Path('sql\\query_spatial_frequency_parameter.sql').read_text(), conn)

        # fetch fluoro settings
        fluoro = pandas.read_sql_query(Path('sql\\query_fluoro_setting.sql').read_text(), conn)

        
        df.insert(1,'hospital_name', f"{hospital_name}-{host_identifier}")
        df["modified"] = modified

        sfp.insert(1,'hospital_name', f"{hospital_name}-{host_identifier}")
        sfp["modified"] = modified

        fluoro.insert(1,'hospital_name', f"{hospital_name}-{host_identifier}")
        fluoro["modified"] = modified

    return df, sfp, fluoro


def parse_db_c_arm(path_to_db: Path, db_version: float, modified: str) -> pandas.DataFrame:

    with sqlite3.connect(path_to_db) as conn:

        if 20.6 <= db_version:
            df = pandas.read_sql_query(Path('sql\\c_arm_dbv206.sql').read_text(), conn)

        df["modified"] = modified

    return df