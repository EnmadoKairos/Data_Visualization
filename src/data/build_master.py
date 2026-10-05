"""
Skeleton for the future canonical object-level dataset builder.

Do not implement source-specific mappings here until the real raw datasets
have been audited. The next project version should turn the harmonization
decisions into deterministic code.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


CANONICAL_COLUMNS = [
    "object_id",
    "object_name",
    "object_type",
    "object_class",
    "active_status",
    "launch_date",
    "decay_date",
    "country",
    "operator",
    "perigee_km",
    "apogee_km",
    "mean_altitude_km",
    "orbit_region",
    "launch_year",
    "altitude_band",
]


def empty_master() -> pd.DataFrame:
    """Return an empty dataframe with the intended first canonical schema."""
    return pd.DataFrame(columns=CANONICAL_COLUMNS)


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "objects_master_template.csv"
    empty_master().to_csv(out, index=False)
    print(f"Wrote template to {out}")
