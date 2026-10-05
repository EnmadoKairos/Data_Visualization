from __future__ import annotations

from pathlib import Path
import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".parquet"}

ID_HINTS = (
    "norad",
    "catalog",
    "cat id",
    "cat_id",
    "object_id",
    "satcat",
)

DATE_HINTS = (
    "launch",
    "decay",
    "date",
    "epoch",
)

TYPE_HINTS = (
    "object type",
    "object_type",
    "type",
    "status",
    "class",
)

ALTITUDE_HINTS = (
    "perigee",
    "apogee",
    "altitude",
    "alt",
)


def discover_files(folder: str | Path) -> list[Path]:
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def load_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t", low_memory=False)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)

    raise ValueError(f"Unsupported file type: {path}")


def matching_columns(df: pd.DataFrame, hints: tuple[str, ...]) -> list[str]:
    cols = []
    for c in df.columns:
        lc = str(c).lower()
        if any(h in lc for h in hints):
            cols.append(c)
    return cols


def audit_dataframe(df: pd.DataFrame, source_name: str = "dataset") -> dict:
    missing = (
        df.isna()
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .round(2)
    )

    duplicate_rows = int(df.duplicated().sum())

    return {
        "source": source_name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicate_rows": duplicate_rows,
        "id_candidates": matching_columns(df, ID_HINTS),
        "date_candidates": matching_columns(df, DATE_HINTS),
        "type_candidates": matching_columns(df, TYPE_HINTS),
        "altitude_candidates": matching_columns(df, ALTITUDE_HINTS),
        "missing_pct": missing.to_dict(),
    }


def compact_summary(audit: dict) -> pd.DataFrame:
    return pd.DataFrame({
        "metric": [
            "rows",
            "columns",
            "duplicate_rows",
            "id_candidates",
            "date_candidates",
            "type_candidates",
            "altitude_candidates",
        ],
        "value": [
            audit["rows"],
            audit["columns"],
            audit["duplicate_rows"],
            ", ".join(map(str, audit["id_candidates"])) or "—",
            ", ".join(map(str, audit["date_candidates"])) or "—",
            ", ".join(map(str, audit["type_candidates"])) or "—",
            ", ".join(map(str, audit["altitude_candidates"])) or "—",
        ],
    })
