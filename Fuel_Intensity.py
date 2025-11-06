import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Example variable definitions (replace with your actual data)
average_speed =  26  # Average speed km/h
class_i = 0       # Class value for observation i (e.g., categorical encoded as integer or dummy)
D_class = 0         # Coefficient for class_i
epsilon_i = 0     # Error term for observation i


########### EVessel Correction Factor - from Gucwa Paper##########
Vessel_class = {
    'Container Ships' : 0.01,
    'LNG Carriers' : 0.39,
    'Product Tankers' : 0.56,
}

########## Capacity Utilization ##########
Capacity_utilization = {
    'Container Ships' : 0.8,
    'Bulk Carriers' : 0.7,
    'Oil Tankers' : 0.7,
}

cap = np.mean(list(Capacity_utilization.values()))  # Example capacity utilizatio




# Shipping Energy Intensity Function
def shipping_EI(cap,load,class_i,D_class, average_speed):
    Gamma = cap*load
    C = -1.051               # Intercept
    beta = -0.589              # Coefficient for log(Gamma)
    gamma = 1.416            # Coefficient for log(average_speed)   
    epsilon_i = 0     # Error term for observation i

    log_E_over_RTK_t = C + beta * np.log(Gamma) + gamma * np.log(average_speed) + D_class * class_i + epsilon_i
    # convert from log(E/RTK) back to normal scale
    E_over_RTK_t = np.exp(log_E_over_RTK_t)
    return E_over_RTK_t, log_E_over_RTK_t




######################################## Plot graph 
# create a range for Gamma and compute the log(E/Rtk) for plotting (avoid log(0) with eps)
load_list = np.logspace(0, 2.3, 200)  # 0.01 .. 100  # ensure positive
log_EI_vals = shipping_EI(cap,load_list, 1, 0, average_speed)[0]  # get log(E/RTK) values for plotting
EI_Vals = shipping_EI(cap,load_list, 1, 0, average_speed)[1]  # get E/RTK values for plotting

plt.figure(figsize=(8, 6))
#plt.plot(load_list, log_EI_vals)                   # <-- single line that plots the equation vs Gamma
plt.plot(load_list, EI_Vals, color='orange')                   # <-- single line that plots the equation vs Gamma
import matplotlib.ticker as mticker

plt.xscale('log')
plt.yscale('log')

ax = plt.gca()
# Option A: keep automatic ticks but force plain (non-exponential) formatting
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x:g}"))
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
# show more ticks on log-log axes: denser major ticks and visible minor ticks
ax.xaxis.set_major_locator(mticker.LogLocator(base=10.0, numticks=15))
ax.xaxis.set_minor_locator(mticker.LogLocator(base=10.0, subs=np.arange(1,10), numticks=50))
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x:g}"))
ax.xaxis.set_minor_formatter(mticker.NullFormatter())

ax.yaxis.set_major_locator(mticker.LogLocator(base=10.0, numticks=15))
ax.yaxis.set_minor_locator(mticker.LogLocator(base=10.0, subs=np.arange(1,10), numticks=50))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, pos: f"{y:g}"))
ax.yaxis.set_minor_formatter(mticker.NullFormatter())

# Make ticks more visible
ax.tick_params(axis='both', which='major', length=6, width=1)
ax.tick_params(axis='both', which='minor', length=3, width=0.8)


plt.xlabel('Load Factor in thousands of Tonnes')
plt.ylabel('EI [MJ/Tkm]')
plt.title('Load in KG vs EI for Average Speed of {} km/h'.format(average_speed))
plt.grid(True)
plt.show()
# ...existing code...


######## Solving for Breyer et al. 2019 Model ##########