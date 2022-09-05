import pandas as pd
import numpy as np

# Load SpaceX dataset, for data analysis
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)
# Identify and calculate the percentage of the missing values in each attribute
df.isnull().sum() / df.count() * 100
# Identify which columns are numerical and categorical:
df.dtypes

# TASK 1: Calculate the number of launches on each site
# Apply value_counts() on column LaunchSite to determine the number of launches on each site
df['LaunchSite'].value_counts()

# TASK 2: Calculate the number and occurrence of each orbit
# Apply value_counts on Orbit column to determine the number and occurance of each orbit
df['Orbit'].value_counts()

# TASK 3: Calculate the number and occurence of mission outcome per orbit type
# landing_outcomes = values on Outcome column
landing_outcomes = df['Outcome'].value_counts()
landing_outcomes

for i, outcome in enumerate(landing_outcomes.keys()):
    print(i, outcome)

bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
bad_outcomes

# TASK 4: Create a landing outcome label from Outcome column
# landing_class = 0 if bad_outcome
# landing_class = 1 otherwise
landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)

df['Class'] = landing_class
df[['Class']].head(8)
df.head(7)

# We can use the following line of code to determine the success rate:
df["Class"].mean()
