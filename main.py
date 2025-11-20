from parse_db import parse_db
import sys
from zipfile import ZipFile
from pathlib import Path


def _find_files_of_specified_type_recursively(input_directory: Path, file_type: str) -> list[Path]:
    dbs: list[Path] = [
        filepath
        for filepath in input_directory.rglob("*")
        if filepath.suffix == file_type
    ]
    return dbs


def main(input_directory: Path):
    print(f'input_directory: {input_directory}')

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
    for sqlite in sqlites:
        print(sqlite)
        # parse sqlite database
        df, sfp = parse_db(sqlite)

        # save dataframe as csv
        df.to_csv(sqlite.with_suffix('.csv'), sep=";", decimal=",", encoding='latin1')
        sfp.to_csv(sqlite.with_name(sqlite.stem + '_sfp').with_suffix('.csv'), sep=";", decimal=",", encoding='latin1')

if __name__ == "__main__":
    main(
        input_directory=Path(sys.argv[1]),
    )
