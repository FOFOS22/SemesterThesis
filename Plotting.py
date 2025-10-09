from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --- load data ---
HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
csv_path = HERE / "projections" / "projections_all.csv"   # adjust if your filename differs
df = pd.read_csv(csv_path)

# pick the value column (support either name)
value_col = "projected_fuel_demand" if "projected_fuel_demand" in df.columns else "projected_fuel_demand_l"
if value_col not in df.columns:
    raise ValueError("Could not find projected fuel column. Expected 'projected_fuel_demand' or 'projected_fuel_demand_l'.")

# clean + sort
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
df = df.dropna(subset=["country", "year", value_col]).sort_values(["country", "year"])

# --- plot ---
plt.figure(figsize=(11, 6))
for country, g in df.groupby("country"):
    plt.plot(g["year"], g[value_col], label=country, linewidth=2)

plt.title("Projected Fuel Demand by Country")
plt.xlabel("Year")
plt.ylabel("Projected Fuel Demand")
plt.grid(True, alpha=0.3)
# put the legend outside if there are many countries
plt.legend(title="Country", bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.)
plt.tight_layout()
plt.show()

# (optional) save the figure
# plt.savefig(HERE / "projections_all_countries.png", dpi=200, bbox_inches="tight")
