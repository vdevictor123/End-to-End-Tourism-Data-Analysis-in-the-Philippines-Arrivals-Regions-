# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:46:22 2026

@author: victor
"""

"""
create_region_coordinates.py
----------------------------
Generate the region_coordinates.xlsx file with the geographic coordinates
of the 16 regions of the Philippines.

The Region_Code and Region_Name values ​​must exactly
match those in the regions_master_CLEAN.xlsx file to allow for the JOIN in Power BI.

Output: region_coordinates.xlsx
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


# ── Datos ────────────────────────────────────────────────────────────────────

REGION_COORDINATES = [
    ("NCR",         "NCR (National Capital Region)",             14.5995, 120.9842),
    ("CAR",         "CAR (Cordillera Administrative Region)",    17.3510, 121.1720),
    ("Region I",    "Region I (ILOCOS REGION)",                  16.0832, 120.6200),
    ("Region II",   "Region II (CAGAYAN VALLEY)",                17.6132, 121.7270),
    ("Region III",  "Region III (CENTRAL LUZON)",                15.4755, 120.5960),
    ("Region IV-A", "Region IV-A CALABARZON",                   14.1008, 121.0794),
    ("Region IV-B", "Region IV-B MIMAROPA",                     10.7202, 121.0794),
    ("Region V",    "Region V (BICOL REGION)",                   13.4213, 123.4136),
    ("Region VI",   "Region VI (WESTERN VISAYAS)",               11.0050, 122.5373),
    ("Region VII",  "Region VII (CENTRAL VISAYAS)",              10.3157, 123.8854),
    ("Region VIII", "Region VIII (EASTERN VISAYAS)",             11.2440, 125.0039),
    ("Region IX",   "Region IX (ZAMBOANGA PENINSULA)",            8.1527, 123.2577),
    ("Region X",    "Region X (NORTHERN MINDANAO)",               8.0220, 124.6220),
    ("Region XI",   "Region XI (DAVAO REGION)",                   7.3041, 125.6800),
    ("Region XII",  "Region XII (SOCCSSARGEN)",                   6.2700, 124.6860),
    ("Region XIII", "Region XIII (CARAGA)",                       8.9456, 125.5450),
]

OUTPUT_PATH = "region_coordinates.xlsx"


# ── Estilos ───────────────────────────────────────────────────────────────────

def header_style():
    return {
        "font":      Font(bold=True, color="FFFFFF", name="Arial", size=11),
        "fill":      PatternFill("solid", start_color="1F4E79"),
        "alignment": Alignment(horizontal="center", vertical="center"),
    }

def thin_border():
    side = Side(style="thin", color="CCCCCC")
    return Border(left=side, right=side, top=side, bottom=side)

def row_fill(row_index):
    color = "EBF3FB" if row_index % 2 == 0 else "FFFFFF"
    return PatternFill("solid", start_color=color)


# ── Construcción del Excel ────────────────────────────────────────────────────

def build_excel(data: list, output_path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Region_Coordinates"

    headers     = ["Region_Code", "Region_Name", "Latitude", "Longitude"]
    col_widths  = [15, 45, 12, 12]
    border      = thin_border()
    h_style     = header_style()

    # Cabecera
    for col, (header, width) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font      = h_style["font"]
        cell.fill      = h_style["fill"]
        cell.alignment = h_style["alignment"]
        cell.border    = border
        ws.column_dimensions[cell.column_letter].width = width
    ws.row_dimensions[1].height = 20

    # Filas de datos
    data_font        = Font(name="Arial", size=10)
    align_center     = Alignment(horizontal="center", vertical="center")
    align_left       = Alignment(horizontal="left",   vertical="center")

    for i, (code, name, lat, lon) in enumerate(data, 2):
        fill   = row_fill(i)
        values = [code, name, lat, lon]
        aligns = [align_center, align_left, align_center, align_center]

        for col, (val, align) in enumerate(zip(values, aligns), 1):
            cell            = ws.cell(row=i, column=col, value=val)
            cell.font       = data_font
            cell.fill       = fill
            cell.alignment  = align
            cell.border     = border

    # Formato numérico para lat/lon
    for row in ws.iter_rows(min_row=2, max_row=len(data) + 1, min_col=3, max_col=4):
        for cell in row:
            cell.number_format = "0.0000"

    ws.freeze_panes = "A2"

    wb.save(output_path)
    print(f"✅ Archivo guardado: {output_path} ({len(data)} regiones)")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_excel(REGION_COORDINATES, OUTPUT_PATH)