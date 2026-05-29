import pandas as pd

df = pd.read_csv("data/Toronto Island Ferry Tickets (1).csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Feature Engineering
df['Hour'] = df['Timestamp'].dt.hour
df['Day'] = df['Timestamp'].dt.day
df['Month'] = df['Timestamp'].dt.month
df['Year'] = df['Timestamp'].dt.year
df['Day_of_Week'] = df['Timestamp'].dt.day_name()
df['Is_Weekend'] = df['Timestamp'].dt.dayofweek >= 5
df['Season'] = df['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})
df['Is_Peak_Hour'] = df['Hour'].between(8, 18)
df['Total_Tickets'] = df['Redemption Count'] + df['Sales Count']

print("Feature Engineering Done!")
print(df.columns.tolist())
print(df.head(3))
# EDA - Basic Analysis
print("\n--- Busiest Hours ---")
print(df.groupby('Hour')['Total_Tickets'].mean().sort_values(ascending=False).head(5))

print("\n--- Busiest Months ---")
print(df.groupby('Month')['Total_Tickets'].mean().sort_values(ascending=False).head(5))

print("\n--- Weekday vs Weekend ---")
print(df.groupby('Is_Weekend')['Total_Tickets'].mean())

print("\n--- Season Summary ---")
print(df.groupby('Season')['Total_Tickets'].mean().sort_values(ascending=False))