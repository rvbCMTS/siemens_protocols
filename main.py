import sys
import sqlite3
import logging
from zipfile import ZipFile
from pathlib import Path
import pandas as pd

from parse_db import parse_db, parse_db_c_arm
from save_data import save_data
from constants import PEX, SPM, FLUORO, PARAMETERS_FOR_COMPARISON, SHEET_NAME, GROUP_BY_COLUMN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("siemens_protocols")

def _parse_and_save_conventional_data(input_directory: Path, header: pd.DataFrame):
    latest_backup_per_machine = (
        header
        .sort_values("modified", ascending=False)
        .drop_duplicates(subset="host_identifier", keep="first")
        .reset_index(drop=True)
    )

    dfs = []
    sfps= []
    fluoros= []
    for backup in latest_backup_per_machine.itertuples():
        logger.info(f"Parsing conventional data for {backup.backup_path} \t version: {backup.db_version} \t modified: {backup.modified} \t hospital: {backup.hospital_name}")

        df, sfp, fluoro = parse_db(path_to_db=backup.backup_path,
                           db_version=backup.db_version,
                           modified=backup.modified,
                           hospital_name=backup.hospital_name,
                           host_identifier=backup.host_identifier)
        dfs.append(df)
        sfps.append(sfp)
        if not fluoro.empty:
            fluoros.append(fluoro)
    df_main = pd.concat(dfs, ignore_index=True)
    sfp_main = pd.concat(sfps, ignore_index=True)
    fluoro_main = pd.concat(fluoros, ignore_index=True)

    df_main.sort_values([PEX[PARAMETERS_FOR_COMPARISON][GROUP_BY_COLUMN], "hospital_name"], inplace=True)
    df_main = df_main.reset_index()

    sfp_main.sort_values([SPM[PARAMETERS_FOR_COMPARISON][GROUP_BY_COLUMN], "hospital_name"], inplace=True)
    sfp_main = sfp_main.reset_index()
    
    fluoro_main.sort_values([FLUORO[PARAMETERS_FOR_COMPARISON][GROUP_BY_COLUMN][0], "hospital_name"], inplace=True)
    fluoro_main = fluoro_main.reset_index()
    
    latest_backup_per_machine = latest_backup_per_machine[["hospital_name", "host_identifier", "db_version", "modified"]]
    latest_backup_per_machine.sort_values(["hospital_name"], inplace=True)
    latest_backup_per_machine = latest_backup_per_machine.reset_index()
    

    save_data(output_path=input_directory, data=latest_backup_per_machine, sheet_name="Header", parameters_for_comparison=[])
    save_data(output_path=input_directory, data=df_main, sheet_name=PEX[SHEET_NAME], parameters_for_comparison=PEX[PARAMETERS_FOR_COMPARISON])
    save_data(output_path=input_directory, data=sfp_main, sheet_name=SPM[SHEET_NAME], parameters_for_comparison=SPM[PARAMETERS_FOR_COMPARISON])
    save_data(output_path=input_directory, data=fluoro_main, sheet_name=FLUORO[SHEET_NAME], parameters_for_comparison=FLUORO[PARAMETERS_FOR_COMPARISON])


def _parse_and_save_c_arm_data(input_directory: Path, header: pd.DataFrame):

    header = (
        header
        .sort_values("modified", ascending=False)
        .reset_index()
    )

    for backup in header.itertuples():
        logger.info(f"Parsing C-arm data for {backup.backup_path} \t version: {backup.db_version} \t modified: {backup.modified}")
        data = parse_db_c_arm(path_to_db=backup.backup_path,
                           db_version=backup.db_version,
                           modified=backup.modified)
        sheet_name = backup.backup_path.relative_to(input_directory).with_suffix("").as_posix().replace("-","_").replace("/","_").replace("pexDbCustomer","PC").replace("pexDbService","PS")
        save_data(output_path=input_directory, data=header, sheet_name="Header", parameters_for_comparison=[])
        save_data(output_path=input_directory, data=data, sheet_name=sheet_name, parameters_for_comparison=[])


def _find_files_of_specified_type_recursively(input_directory: Path, file_type: str) -> list[Path]:
    dbs: list[Path] = [
        filepath
        for filepath in input_directory.rglob("*")
        if filepath.suffix == file_type
    ]
    return dbs

def _read_pex_database_header(path_to_db: Path) -> dict:
    with sqlite3.connect(path_to_db) as conn:
        c_arm_pex = conn.execute(Path("sql\\table_triplet_exists.sql").read_text()).fetchall()
        c_arm_pex = c_arm_pex[0][0]

        if c_arm_pex:
            cur = conn.execute(Path("sql\\query_header_c_arm.sql").read_text())
        else:
            cur = conn.execute(Path("sql\\query_header.sql").read_text())
        row = cur.fetchall()
        columns = [column[0] for column in cur.description]

    header = dict(zip(columns, row[0]))
    header['type'] = 'c-arm' if c_arm_pex else 'conventional'
    header['backup_path'] = path_to_db
    
    return header


def main(input_directory: Path):
    logger.info(f'input_directory: {input_directory}')

    # find all .zip in input_directory
    zips: list[Path] = _find_files_of_specified_type_recursively(input_directory, '.zip')
    for zip in zips:
        # open zipYe
        with ZipFile(zip, 'r') as z:
            # list of zips with .sqlite file
            file_name = [s for s in z.namelist() if '.sqlite' in s]
            if len(file_name) > 0:
                z.extract(file_name[0], zip.parent)

    # find all .sqlite in input_directory
    sqlites: list[Path] = _find_files_of_specified_type_recursively(input_directory, '.sqlite')

    # Read header of all .sqlite files
    logger.info(f'Reading header for {len(sqlites)} backup file(s)')
    header = pd.DataFrame([_read_pex_database_header(sqlite) for sqlite in sqlites])
    logger.info('Done reading header(s)')

    if not header[header["type"] == "conventional"].empty:
        _parse_and_save_conventional_data(input_directory=input_directory, header=header[header["type"] == "conventional"])
    if not header[header["type"] == "c-arm"].empty:
        _parse_and_save_c_arm_data(input_directory=input_directory, header=header[header["type"] == "c-arm"])
    
    logger.info('Done parsing and saving data')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError(
            f"Usage: {sys.argv[0]} <input_directory>"
        )

    input_directory = Path(sys.argv[1])

    if not input_directory.is_dir():
        raise ValueError(f"Invalid input directory: {input_directory}")

    main(input_directory=input_directory)


