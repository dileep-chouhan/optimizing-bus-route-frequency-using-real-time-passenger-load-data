import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
num_routes = 5
num_days = 30
data = {
    'Route': np.random.choice(['A', 'B', 'C', 'D', 'E'], size=num_days*num_routes),
    'Date': pd.to_datetime(['2024-03-01'] * (num_days*num_routes)) + pd.to_timedelta(np.random.randint(0, num_days, size=num_days*num_routes), unit='D'),
    'Time': pd.to_datetime(np.random.choice(['07:00', '08:00', '09:00', '17:00', '18:00', '19:00'], size=num_days*num_routes), format='%H:%M').time,
    'PassengerLoad': np.random.randint(10, 100, size=num_days*num_routes)
}
df = pd.DataFrame(data)
# --- 2. Data Cleaning and Preparation ---
df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
df = df.drop(['Date', 'Time'], axis=1)
df = df.sort_values(by=['Route', 'DateTime'])
df['Hour'] = df['DateTime'].dt.hour
df['Day'] = df['DateTime'].dt.day
# --- 3. Analysis ---
# Calculate average passenger load per route and hour
average_load = df.groupby(['Route', 'Hour'])['PassengerLoad'].mean().unstack()
# Identify routes and times with high passenger load
high_load_routes = average_load[average_load > 75].stack().index.tolist()
# --- 4. Visualization ---
plt.figure(figsize=(12, 6))
sns.heatmap(average_load, annot=True, cmap="YlGnBu", fmt=".1f")
plt.title('Average Passenger Load per Route and Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Route')
plt.tight_layout()
output_filename = 'passenger_load_heatmap.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")
# --- 5. Recommendations (Example) ---
print("\nRecommendations:")
if high_load_routes:
    for route, hour in high_load_routes:
        print(f"- Increase frequency for Route {route} at {hour}:00.")
else:
    print("- No routes require immediate frequency adjustments based on current data.")