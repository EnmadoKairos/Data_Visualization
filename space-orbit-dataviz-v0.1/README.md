# Orbital Congestion in Low Earth Orbit — Data Visualization Project

Version: **v0.1 — Project scaffold + data audit**

This repository is the first working version of the Data Visualization course project on congestion in Low Earth Orbit (LEO).

## Project goal

The project investigates how the population and composition of artificial objects in Low Earth Orbit have changed over time, with particular attention to:

- active satellites;
- inactive spacecraft and rocket bodies;
- catalogued debris;
- the main actors operating in orbit;
- concentration of objects across altitude bands;
- the distinction between cumulative launches and objects actually remaining in orbit.

The final output is expected to be a **web-based explanatory visualization** with a guided narrative and limited, meaningful interactivity.

## Current milestone

This version intentionally does **not** build the final visualization yet.

The first objective is to answer:

> What data do we actually have, how compatible are the sources, and can they support the project we proposed?

The immediate workflow is:

1. place the raw datasets in `data/raw/`;
2. run the data audit notebook;
3. inspect schemas, identifiers, missingness, duplicates, temporal coverage, and orbital variables;
4. verify whether the sources can be joined reliably;
5. define the canonical object-level schema;
6. only then move on to cleaning, EDA, and visualization design.

## Expected raw sources

### UCS Satellite Database
Place the UCS dataset in:

`data/raw/ucs/`

Expected use:
- active satellites;
- operator / owner;
- country;
- purpose / mission;
- launch date;
- orbit-related metadata;
- expected lifetime where available.

### CelesTrak / SATCAT / GP data
Place the downloaded catalogue data in:

`data/raw/celestrak/`

Expected use:
- catalogued orbital objects;
- object identifiers;
- object type;
- launch date;
- decay date;
- orbital parameters;
- active / inactive / debris-related classification where derivable.

### ESA Space Environment material
Place reports, extracts, or manually curated aggregate tables in:

`data/raw/esa/`

Expected use:
- authoritative definitions;
- aggregate statistics;
- contextual events;
- limitations and sustainability framing.

## Canonical schema — first target

The first processed table should eventually contain one row per catalogued object, with fields similar to:

| Variable | Meaning |
|---|---|
| `object_id` | Stable catalogue identifier, preferably NORAD CAT ID when available |
| `object_name` | Object name |
| `object_type` | Harmonized type |
| `active_status` | Active / inactive / unknown |
| `launch_date` | Launch date |
| `decay_date` | Decay date if applicable |
| `country` | Country / owner grouping |
| `operator` | Operator / owning organization |
| `perigee_km` | Perigee altitude |
| `apogee_km` | Apogee altitude |
| `mean_altitude_km` | Derived mean altitude |
| `orbit_region` | LEO / other |
| `launch_year` | Derived launch year |
| `altitude_band` | Derived altitude band |
| `object_class` | Simplified analytical category |

The exact schema will be finalized only after auditing the real datasets.

## Definition currently used

For this project, **Low Earth Orbit (LEO)** is defined as the region below **2,000 km**.

The project will distinguish between:
- active satellites;
- inactive spacecraft / rocket bodies;
- catalogued debris.

This repository should never silently equate:
- cumulative launches,
- catalogued historical objects,
- and objects currently remaining in orbit.

## First notebook

Open:

`notebooks/01_data_audit.ipynb`

It is designed to:
- discover candidate raw files;
- load CSV / TSV / Excel files;
- report dimensions and columns;
- inspect missing values;
- detect duplicated identifiers;
- inspect candidate NORAD / catalogue identifier fields;
- inspect date coverage;
- inspect possible object-type and orbital-altitude columns;
- produce a compact audit summary.

## Python environment

Recommended Python version: **3.11+**

Install dependencies:

```bash
pip install -r requirements.txt
```

Then launch:

```bash
jupyter lab
```

## Reproducibility

Raw data should not be modified manually after download.

The intended pipeline is:

`data/raw/` → `data/interim/` → `data/processed/`

All transformations should eventually be reproducible from code.

## Next milestone after v0.1

Once the real UCS and CelesTrak/SATCAT datasets are added, the next version should:

1. establish reliable join keys;
2. harmonize object classes;
3. harmonize country/operator names;
4. parse launch and decay dates;
5. derive LEO membership and altitude bands;
6. create the first `objects_master` dataset;
7. perform the first substantive EDA.
