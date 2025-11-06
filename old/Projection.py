from pathlib import Path
import pandas as pd

################################### read csv file ###################################
HERE = Path(__file__).resolve().parent
data_baseline = pd.read_csv(HERE / "Status Quo" / "statusQuo_2023_cleaned.csv")

def five_year_steps(start=2023, end=2050, include_unaligned_end=False):
    years = list(range(start, end + 1, 5))  # 2023, 2028, 2033, ...
    if include_unaligned_end and years and years[-1] != end:
        years.append(end)
    return years

############################ set up projection ###################################
growth_rate = 0.02  # 2% annual growth (fraction, not percent)

####################### Time frame for projection ##########################
years = five_year_steps(2023, 2050)

# (Optional) where to put outputs
out_dir = HERE / "projections"
out_dir.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in str(s)).strip("_").lower()

# If your CSV might have multiple rows per country, aggregate the baseline:
baseline_by_country = (
    data_baseline
    .groupby("country", dropna=False)["median"]
    .sum()
)

for Country, base_val in baseline_by_country.items():
    # Build a fresh projection table for THIS country
    df_country = pd.DataFrame({"year": years})
    # Years elapsed since baseline (2023)
    t = df_country["year"] - 2023
    # Compound annually from the 2023 baseline value
    df_country["projected_fuel_demand"] = (float(base_val) * ((1 + growth_rate) ** t)).round(2)

    # (Optional) include some context columns
    df_country.insert(0, "country", Country)
    df_country.insert(1, "baseline_year", 2023)
    df_country.insert(2, "baseline_fuel_l", float(base_val))
    df_country["annual_growth_rate"] = growth_rate  # as fraction (0.02 = 2%)

    # Safe filename per country
    output_path = out_dir / f"projections_{slugify(Country)}.csv"
    df_country.to_csv(output_path, index=False)
    print(f"Wrote {output_path}")

############################ stich all countries together ############################

out_path = HERE / "projections" / "projections_all.csv"
in_dir = HERE / "projections"

# Grab all CSVs (adjust the pattern if needed)
files = sorted(in_dir.glob("*.csv"))
if not files:
    raise SystemExit(f"No CSVs found in {in_dir}")

# Simple vertical stack
merged = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Save
merged.to_csv(out_path, index=False)  # add float_format="%.2f" if you want fixed decimals
print(f"Wrote {out_path} with {len(merged)} rows from {len(files)} files.")