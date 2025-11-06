import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import norm

# Create directory if it doesn't exist
os.makedirs('Status Quo', exist_ok=True)

# Fetch the data.
df = pd.read_csv("https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadata = requests.get("https://ourworldindata.org/grapher/gdp-per-capita-worldbank.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

Countries = ["Papua New Guinea", "Solomon Islands", "Vanuatu", "Fiji", "Samoa", "Tonga", "Cook Islands", "Marshall Islands", "Micronesia (Federated States of)"]

# Filter the DataFrame to include only the specified countries
filtered_df = df[df['Entity'].isin(Countries)].copy()
filtered_df['pct_change'] = (
    filtered_df.groupby('Entity')['ny_gdp_pcap_pp_kd']
    .pct_change(fill_method=None) * 100
)
filtered_df["pct_change"] = filtered_df["pct_change"].round(2)

print(filtered_df.head())


filtered_df.to_csv('Status Quo/percent_change_by_country.csv', index=False)



# Compute average pct_change per year across all countries
yearly_stats = filtered_df.groupby('Year')['pct_change'].agg(['mean', 'std']).reset_index()
yearly_stats['mean'] = yearly_stats['mean'].round(2)
yearly_stats['std'] = yearly_stats['std'].round(2)
avg_gdp = filtered_df.groupby('Year')['ny_gdp_pcap_pp_kd'].mean().round(2).reset_index().rename(columns={'ny_gdp_pcap_pp_kd': 'avg_gdp'})
yearly_stats = yearly_stats.merge(avg_gdp, on='Year', how='left')
print("These are the yearly stats:\n", yearly_stats)
print('-' * 50)  # Separation line
print("These are the average stats:\n", "Average GDP growth 1990-2023:  ", yearly_stats['mean'].mean().round(2),"\n Country Standard Deviation of GDP growth 1990-2023: ", yearly_stats['std'].mean().round(2))

###################################### Pause here ##########################################1

print("Step 1 complete.")

# Pause and wait for user to continue or exit
while True:
    user_input = input("Enter 1 to continue or 2 to exit: ")
    if user_input == "1":
        break

    elif user_input == "2":
        print("Exiting the program.")
        exit()
    else:
        print("Invalid input. Please enter 1 to continue or 2 to exit.")

# Continue
print("Step 2 starting...")

########################################## Plotting ##########################################

################## PLOT 1: Plot country lines (same as before)
plt.figure(figsize=(10, 6))
for country, group in filtered_df.groupby('Entity'):
    plt.plot(group['Year'], group['pct_change'], marker='o', label=country, alpha=0.6)


# Plot average line with error bars
plt.errorbar(
    yearly_stats['Year'],
    yearly_stats['mean'],
    yerr=yearly_stats['std'],
    fmt='--D',
    color='black',
    label='Average ± Std Dev',
    capsize=5
)
# Labels and styling
plt.xlabel('Year')
plt.ylabel('Percentage Change (%)')
plt.title('Yearly Percentage Change by Country with Average Line')
plt.legend(title='Country')
plt.grid(True)
plt.tight_layout()


################ PLOT 2: Plot GDP per capita with average line
plt.figure(figsize=(10, 6))
for country, group in filtered_df.groupby('Entity'):
    plt.plot(group['Year'], group['ny_gdp_pcap_pp_kd'], marker='o', label=country, alpha=0.6)

# Plot average line
plt.plot(yearly_stats['Year'], yearly_stats['avg_gdp'], marker='D', linestyle='dashed', color='black', label='Average')

# Labels and styling
plt.xlabel('Year')
plt.ylabel('GDP per Capita (constant 2017 international $)')
plt.title('Yearly GDP per Capita by Country with Mean Line')
plt.legend(title='Country')
plt.grid(True)
plt.tight_layout()


################ PLOT 3: Bell curve fit to data
plt.figure(figsize=(10, 6))
# Plot histogram of the mean percentage changes with bins matching the actual data values
plt.hist(yearly_stats['mean'], bins=np.sort(yearly_stats['mean'].unique()), density=True, alpha=0.6, color='blue', label='Data')

# Calculate mean and standard deviation for the fit
mu = yearly_stats['mean'].mean()
std = yearly_stats['mean'].std()

# Plot the fitted normal curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 1000)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2, label=f'Fit: μ={mu:.2f}, standard deviation of GDP Growth values={std:.2f}')
plt.vlines(mu, 0, max(p), colors='r', linestyles='dashed', label='Mean')

plt.title('Bell Curve Fit to Data')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

