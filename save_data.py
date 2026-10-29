from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from constants import PARAMETER_LIST, GROUP_BY_COLUMN
from pathlib import Path
import pandas as pd
import logging

HIGHLIGHT_COLOR = 'FFFF0000'
logger = logging.getLogger("siemens_protocols")

def _format_excel_table(display_name: str, work_sheet: str):
    table = Table(
         displayName=display_name,
         ref=f"A1:{get_column_letter(work_sheet.max_column)}{work_sheet.max_row}",
        )
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9",
        showRowStripes=True,
        showColumnStripes=False
        )
    work_sheet.add_table(table)


def _analyze_data_for_harmonization(data: pd.DataFrame, parameters_for_comparison: dict, work_sheet: str) -> pd.DataFrame:

    highlight_fill = PatternFill(
        start_color=HIGHLIGHT_COLOR,
        end_color=HIGHLIGHT_COLOR,
        fill_type="solid",
    )

    grp = data.groupby(parameters_for_comparison[GROUP_BY_COLUMN])


    for param in parameters_for_comparison[PARAMETER_LIST]:
        mode_per_group = grp[param].agg(
            lambda s: s.mode(dropna=True).iloc[0]
            if not s.mode(dropna=True).empty else pd.NA
        ).dropna()

        mode_mapped = (
            data.merge(
                mode_per_group.rename('mode_value'),
                left_on=parameters_for_comparison[GROUP_BY_COLUMN],
                right_index=True,
                how='left'
            )['mode_value']
        )

        flag = (
            data[param].notna()
            & mode_mapped.notna()
            & (data[param] != mode_mapped)
        )

        col_idx = data.columns.get_loc(param)
        for row_idx in data.index[flag]:
            work_sheet.cell(row=row_idx + 2, column=col_idx + 1).fill = highlight_fill

    return data



def save_data(output_path: Path, data: pd.DataFrame, sheet_name: str, parameters_for_comparison: dict):
    logger.info(f"Writing data to Excel for sheet: {sheet_name}")
    output_path = output_path.joinpath(f"Pex_{output_path.name}_{pd.Timestamp.now().strftime('%Y-%m-%d')}").with_suffix('.xlsx')

    if not output_path.exists():
        with pd.ExcelWriter(output_path, mode="w", engine='openpyxl') as writer:
            data.to_excel(writer,
                        sheet_name=sheet_name,
                        index=False,
            )
    else:
        with pd.ExcelWriter(output_path, mode="a", engine='openpyxl', if_sheet_exists="replace") as writer:
            data.to_excel(writer,
                        sheet_name=sheet_name,
                        index=False,
            )
           
    wb = load_workbook(output_path)
    work_sheet = wb[sheet_name]
    _format_excel_table(display_name=f"T{sheet_name}", work_sheet=work_sheet)
    if parameters_for_comparison:
        _analyze_data_for_harmonization(data=data, parameters_for_comparison=parameters_for_comparison, work_sheet=work_sheet)

    wb.save(output_path)