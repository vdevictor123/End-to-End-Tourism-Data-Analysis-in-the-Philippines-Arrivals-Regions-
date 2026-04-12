"""
Script: extract_pdf_to_excel.py
Descripcion: Extrae datos de turismo de TODOS los PDFs de Filipinas (2015-2023)
             y guarda un Excel por anno: Philippines_Tourism_YYYY.xlsx

             Logica de clasificacion (validada contra todos los PDFs):
               - Region   : unica linea con SOLO fuentes Bold Y nombre de region
               - Province : only_bold=False, x0 intermedio (segundo cluster tras Region)
               - City/Mun : only_bold=False, x0 mayor (tercer cluster)
               Los umbrales de x0 se detectan automaticamente por cada PDF.

             Correcciones de datos:
               - Total recalculado cuando esta vacio o inconsistente
               - Valores negativos eliminados (clip a 0)
               - Dashes (-) que representan ceros tratados correctamente

Uso:
    python extract_pdf_to_excel.py

Dependencias:
    pip install pdfplumber openpyxl
"""

import re
import pdfplumber
import openpyxl
from pathlib import Path
from collections import Counter

# ─── CONFIGURACION ─────────────────────────────────────────────────────────────

PDF_DIR    = r"C:\Users\victor\Desktop\Nueva carpeta (2)\PDF"
OUTPUT_DIR = r"C:\Users\victor\Desktop\Nueva carpeta (2)\Excel"

# Patron de nombre de region
REGION_PATTERN = re.compile(
    r"NCR|CAR|Region\s+(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|IV-A|IV-B)",
    re.IGNORECASE
)

# Lista oficial de las 81 provincias de Filipinas (+ variantes de nombre usadas en los PDFs)
# Estas entradas se clasifican como "Province" independientemente de su x0.
PH_PROVINCES: set[str] = {
    # CAR
    "Abra", "Apayao", "Benguet", "Ifugao", "Kalinga", "Mountain Province",
    # Region I
    "Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan",
    # Region II
    "Batanes", "Cagayan", "Isabela", "Nueva Vizcaya", "Quirino",
    # Region III
    "Aurora", "Bataan", "Bulacan", "Nueva Ecija", "Pampanga", "Tarlac", "Zambales",
    # Region IV-A
    "Batangas", "Cavite", "Laguna", "Quezon", "Rizal",
    # Region IV-B
    "Marinduque", "Occidental Mindoro", "Oriental Mindoro", "Palawan", "Romblon",
    # Region V
    "Albay", "Camarines Norte", "Camarines Sur", "Catanduanes", "Masbate", "Sorsogon",
    # Region VI
    "Aklan", "Antique", "Capiz", "Guimaras", "Iloilo", "Negros Occidental",
    # Region VII
    "Bohol", "Cebu", "Negros Oriental", "Siquijor",
    # Region VIII
    "Biliran", "Eastern Samar", "Leyte", "Northern Samar",
    "Samar", "Western Samar", "Southern Leyte",
    # Region IX
    "Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay",
    # Region X
    "Bukidnon", "Camiguin", "Lanao del Norte", "Misamis Occidental", "Misamis Oriental",
    # Region XI
    "Compostela Valley", "Davao de Oro", "Davao del Norte",
    "Davao del Sur", "Davao Occidental", "Davao Oriental",
    # Region XII
    "Cotabato", "North Cotabato", "Sarangani", "South Cotabato", "Sultan Kudarat",
    # Region XIII
    "Agusan del Norte", "Agusan del Sur", "Dinagat Islands",
    "Surigao del Norte", "Surigao del Sur",
    # BARMM/ARMM
    "Basilan", "Lanao del Sur", "Maguindanao", "Sulu", "Tawi-Tawi",
    # Variantes de nombre usadas en los PDFs
    "Masbate Province",
}

# Ciudades independientes / altamente urbanizadas que aparecen al nivel de provincia en el PDF
# (sin estar dentro de ninguna provincia, como Baguio City en CAR o Cotabato City en XII)
STANDALONE_CITIES_AS_PROVINCE: set[str] = {
    "Baguio City",
    "Cotabato City",
    "Isabela City",
}

# Palabras clave para saltar lineas de cabecera / pie
SKIP_KEYWORDS = [
    "DISTRIBUTION OF REGIONAL",
    "REGIONAL DISTRIBUTION",
    "January-December",
    "JANUARY",
    "DECEMBER",
    "Partial Report",
    "Region/Province/City",
    "Source of Data",
    "Prepared by",
    "As of",
    "GRAND TOTAL",
    "Travelers",
    "Travellers",
    "Filipinos",
    "Foreign",
    "Domestic",
    "Overseas",
]

# ─── FUNCIONES ─────────────────────────────────────────────────────────────────

def parse_number(text: str) -> int:
    """Convierte texto numerico a entero. Nunca devuelve negativo."""
    if not text:
        return 0
    cleaned = text.strip().replace(",", "").replace(" ", "")
    if cleaned in ("-", "", "0"):
        return 0
    try:
        return max(0, int(float(cleaned)))
    except ValueError:
        return 0


def get_region_code(region_name: str) -> str:
    """Extrae el codigo de region del nombre completo."""
    patterns = [
        (r"NCR",            "NCR"),
        (r"\bCAR\b",        "CAR"),
        (r"Region\s+IV-A",  "Region IV-A"),
        (r"Region\s+IV-B",  "Region IV-B"),
        (r"Region\s+XIII",  "Region XIII"),
        (r"Region\s+XII",   "Region XII"),
        (r"Region\s+XI",    "Region XI"),
        (r"Region\s+X\b",   "Region X"),
        (r"Region\s+IX",    "Region IX"),
        (r"Region\s+VIII",  "Region VIII"),
        (r"Region\s+VII",   "Region VII"),
        (r"Region\s+VI",    "Region VI"),
        (r"Region\s+V\b",   "Region V"),
        (r"Region\s+IV\b",  "Region IV"),
        (r"Region\s+III",   "Region III"),
        (r"Region\s+II\b",  "Region II"),
        (r"Region\s+I\b",   "Region I"),
    ]
    for pattern, code in patterns:
        if re.search(pattern, region_name, re.IGNORECASE):
            return code
    return region_name.split()[0]


def should_skip(name: str) -> bool:
    """Determina si una linea debe omitirse."""
    name_upper = name.upper()
    for kw in SKIP_KEYWORDS:
        if kw.upper() in name_upper:
            return True
    return False


def detect_column_boundaries(page) -> tuple[float, float, float]:
    """
    Detecta los limites de columna automaticamente desde la cabecera del PDF.
    Devuelve (fo_boundary, od_boundary, dt_boundary).
    Clasificacion por CENTRO del word:
      center < fo  -> foreign
      fo <= center < od  -> overseas
      od <= center < dt  -> domestic
      center >= dt       -> total
    """
    words = page.extract_words()
    centers: dict[str, float] = {}

    for w in words:
        t = w["text"].upper()
        cx = (w["x0"] + w["x1"]) / 2
        if t == "FOREIGN" and "F" not in centers:
            centers["F"] = cx
        elif t in ("FILIPINOS", "OVERSEAS") and "O" not in centers:
            centers["O"] = cx
        elif t == "DOMESTIC" and "D" not in centers:
            centers["D"] = cx
        elif t == "TOTAL" and "T" not in centers:
            centers["T"] = cx

    if "F" in centers and "O" in centers and "D" in centers:
        t_center = centers.get("T", centers["D"] + 80)
        fo = (centers["F"] + centers["O"]) / 2
        od = (centers["O"] + centers["D"]) / 2
        dt = (centers["D"] + t_center) / 2
        return fo, od, dt

    # Fallback si la cabecera no se detecta
    return 297.0, 365.0, 430.0


def classify_center(cx: float, fo: float, od: float, dt: float) -> str:
    """Clasifica el centro de un word en su columna numerica."""
    if cx < fo:
        return "foreign"
    if cx < od:
        return "overseas"
    if cx < dt:
        return "domestic"
    return "total"


MIN_GAP_PX = 6  # Gap minimo (px) para que el umbral x0 sea fiable


def detect_level_thresholds(raw_rows: list[dict]) -> float | None:
    """
    Detecta automaticamente el umbral de x0 que separa Province de City/Municipality.

    Estrategia:
      1. Calcula region_x0 = x0 minimo de las filas de Region (only_bold + nombre de region)
      2. Recoge todos los x0 de filas no-Region, filtrando outliers grandes
      3. Busca el mayor salto (gap) entre valores consecutivos de x0
      4. El umbral = punto medio de ese salto

    Devuelve el umbral si el gap es suficientemente grande (>= MIN_GAP_PX),
    o None si el gap es demasiado pequeno para ser fiable (fallback: solo usar nombres).
    """
    region_x0_vals = []
    non_region_x0_vals = []

    for row in raw_rows:
        if row["only_bold"] and REGION_PATTERN.search(row["name"]):
            region_x0_vals.append(row["x0"])
        else:
            non_region_x0_vals.append(row["x0"])

    if not region_x0_vals:
        return None

    region_x0 = min(region_x0_vals)

    # Filtrar x0 no-region: deben estar en un rango razonable respecto a region_x0.
    # Los textos de cabecera (año, "As of May", etc.) tienen x0 mucho mayor.
    # En todos los PDFs, ciudad/municipio tiene x0 < region_x0 + 120.
    max_x0 = region_x0 + 120
    filtered = sorted(set(
        round(x, 0)
        for x in non_region_x0_vals
        if region_x0 < x < max_x0
    ))

    if len(filtered) < 2:
        # Solo hay un nivel por debajo de Region -> todo es City
        return None

    # Buscar el mayor salto entre valores consecutivos
    gaps = [(filtered[i + 1] - filtered[i], i) for i in range(len(filtered) - 1)]
    max_gap, max_gap_idx = max(gaps, key=lambda g: g[0])

    if max_gap < MIN_GAP_PX:
        # Gap demasiado pequeno: umbral no es fiable, usar solo nombres
        return None

    province_max = filtered[max_gap_idx]
    city_min     = filtered[max_gap_idx + 1]
    threshold    = (province_max + city_min) / 2

    return threshold


def parse_pdf(pdf_path: str, year: int) -> list[dict]:
    """
    Lee el PDF y devuelve filas estructuradas con:
      name, x0, only_bold, foreign, overseas, domestic, total
    """
    raw_rows = []
    fo = od = dt = None  # limites de columna (se detectan en pagina 0)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):

            if page_num == 0:
                fo, od, dt = detect_column_boundaries(page)

            # Agrupar caracteres por linea para detectar fuentes
            char_lines: dict[float, list] = {}
            for c in page.chars:
                top = round(c["top"], 0)
                char_lines.setdefault(top, []).append(c)

            # Agrupar words por linea
            word_lines: dict[float, list] = {}
            for w in page.extract_words():
                top = round(w["top"], 0)
                word_lines.setdefault(top, []).append(w)

            for top in sorted(word_lines):
                ws = word_lines[top]
                if not ws:
                    continue

                # Detectar fuentes en la linea
                cs = char_lines.get(top, [])
                fonts = {c["fontname"] for c in cs if c["text"].strip()}
                bold_fonts    = {f for f in fonts if "Bold" in f}
                nonbold_fonts = {f for f in fonts if "Bold" not in f}
                only_bold = bool(bold_fonts) and not nonbold_fonts

                name_words: list = []
                cols: dict[str, list[str]] = {
                    "foreign": [], "overseas": [], "domestic": [], "total": []
                }

                for w in ws:
                    cx = (w["x0"] + w["x1"]) / 2
                    if any(ch.isdigit() for ch in w["text"]):
                        col = classify_center(cx, fo, od, dt)
                        cols[col].append(w["text"])
                    elif w["text"] not in ("-",):
                        # Los guiones (-) representan 0; los excluimos del nombre
                        name_words.append(w)

                name = " ".join(w["text"] for w in name_words).strip()
                if not name or should_skip(name):
                    continue

                x0 = name_words[0]["x0"] if name_words else 0

                foreign  = parse_number("".join(cols["foreign"]))
                overseas = parse_number("".join(cols["overseas"]))
                domestic = parse_number("".join(cols["domestic"]))
                total    = parse_number("".join(cols["total"]))

                computed = foreign + overseas + domestic

                # Corregir Total vacio o claramente incorrecto
                if total == 0 and computed > 0:
                    total = computed
                elif total > 0 and computed > 0:
                    ratio = computed / total
                    if ratio < 0.5 or ratio > 2.0:
                        total = computed

                # Descartar filas completamente vacias
                if foreign == 0 and overseas == 0 and domestic == 0:
                    continue

                raw_rows.append({
                    "name":      name,
                    "x0":        x0,
                    "only_bold": only_bold,
                    "foreign":   foreign,
                    "overseas":  overseas,
                    "domestic":  domestic,
                    "total":     total,
                })

    return raw_rows


def build_excel_rows(raw_rows: list[dict], year: int) -> list[dict]:
    """
    Clasifica cada fila en Region / Province / City/Municipality
    usando umbrales de x0 detectados automaticamente.
    """
    if not raw_rows:
        return []

    # Detectar umbral Province vs City para este PDF
    province_threshold = detect_level_thresholds(raw_rows)

    excel_rows         = []
    current_region_code = None
    current_region_name = None
    current_province    = None

    for row in raw_rows:
        name      = row["name"]
        x0        = row["x0"]
        only_bold = row["only_bold"]

        # ── CLASIFICACION ────────────────────────────────────────────────────
        if only_bold and REGION_PATTERN.search(name):
            # REGION
            level               = "Region"
            current_region_code = get_region_code(name)
            current_region_name = name
            current_province    = None
            province_col        = None

        elif (
            name in PH_PROVINCES
            or name.replace(" Province", "") in PH_PROVINCES
            or name in STANDALONE_CITIES_AS_PROVINCE
            or (province_threshold is not None and x0 < province_threshold)
        ):
            # PROVINCE: nombre oficial O x0 intermedio fiable (gap >= MIN_GAP_PX)
            level            = "Province"
            current_province = name
            province_col     = name

        else:
            # CITY / MUNICIPALITY
            level        = "City/Municipality"
            province_col = current_province

        # Descartar filas que aparecen antes de la primera region
        if current_region_code is None and level != "Region":
            continue

        excel_rows.append({
            "year":        year,
            "region_code": current_region_code,
            "region_name": current_region_name,
            "province":    province_col if level != "Region" else None,
            "location":    name,
            "level":       level,
            "foreign":     row["foreign"],
            "ofw":         row["overseas"],
            "domestic":    row["domestic"],
            "total":       row["total"],
        })

    return excel_rows


def write_excel(excel_rows: list[dict], output_path: str) -> None:
    """Escribe los datos en un archivo Excel."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    headers = [
        "Year", "Region_Code", "Region_Name", "Province",
        "Location", "Level",
        "Foreign_Travelers", "OFW", "Domestic_Travelers", "Total",
    ]
    ws.append(headers)

    for row in excel_rows:
        ws.append([
            row["year"],
            row["region_code"],
            row["region_name"],
            row["province"],
            row["location"],
            row["level"],
            row["foreign"],
            row["ofw"],
            row["domestic"],
            row["total"],
        ])

    col_widths = [6, 12, 45, 30, 35, 18, 18, 10, 18, 14]
    for i, width in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    wb.save(output_path)


def get_year_from_filename(filename: str) -> int | None:
    """Extrae el anno del nombre del archivo (ej: '2023_ok.pdf' -> 2023)."""
    match = re.search(r"(\d{4})", filename)
    return int(match.group(1)) if match else None


# ─── EJECUCION PRINCIPAL ────────────────────────────────────────────────────────

def main():
    pdf_dir    = Path(PDF_DIR)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(pdf_dir.glob("*.pdf"), key=lambda p: p.name)
    if not pdf_files:
        print(f"No se encontraron PDFs en: {pdf_dir}")
        return

    print(f"PDFs encontrados: {[p.name for p in pdf_files]}")
    print("=" * 65)

    summary = []

    for pdf_path in pdf_files:
        year = get_year_from_filename(pdf_path.name)
        if year is None:
            print(f"  AVISO: no se puede extraer anno de '{pdf_path.name}' -- omitiendo")
            continue

        output_file = f"Philippines_Tourism_{year}.xlsx"
        output_path = output_dir / output_file

        print(f"\nProcesando: {pdf_path.name}  ->  {output_file}")

        raw_rows   = parse_pdf(str(pdf_path), year)
        excel_rows = build_excel_rows(raw_rows, year)

        regions   = sum(1 for r in excel_rows if r["level"] == "Region")
        provinces = sum(1 for r in excel_rows if r["level"] == "Province")
        cities    = sum(1 for r in excel_rows if r["level"] == "City/Municipality")
        bad_total = sum(1 for r in excel_rows if r["total"] == 0)

        print(f"  Regiones: {regions} | Provincias: {provinces} | Ciudades/Municipios: {cities}")
        print(f"  Total filas: {len(excel_rows)} | Filas con Total=0: {bad_total}")

        write_excel(excel_rows, str(output_path))
        print(f"  OK -> {output_path}")

        summary.append((year, regions, provinces, cities, len(excel_rows), bad_total))

    # Resumen final
    print(f"\n{'='*65}")
    print("RESUMEN FINAL")
    print(f"{'Anno':<8} {'Reg':>4} {'Prov':>5} {'City':>6} {'Total':>7} {'Total=0':>8}")
    print("-" * 45)
    for year, reg, prov, city, total, bad in summary:
        estado = "OK" if bad == 0 else f"AVISO:{bad}"
        print(f"{year:<8} {reg:>4} {prov:>5} {city:>6} {total:>7} {estado:>8}")
    print(f"\nExcels guardados en: {output_dir}")


if __name__ == "__main__":
    main()
