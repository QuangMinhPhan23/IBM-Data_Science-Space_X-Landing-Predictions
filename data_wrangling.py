# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)
df.isnull().sum()/len(df)*100
df.dtypes

# TASK 1: Calculate the number of launches on each site
# Apply value_counts() on column LaunchSite
launch_num = df['LaunchSite'].value_counts()


# TASK 2: Calculate the number and occurrence of each orbit
orbit_num = df['Orbit'].value_counts()
print(orbit_num)
orbit_occurrence = df['Orbit'].value_counts(normalize=True)

# TASK 3: Calculate the number and occurence of mission outcome of the orbits
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
# create a set of outcomes where the second stage did not land successfully:
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])

# TASK 4: Create a landing outcome label from Outcome column
# Using the Outcome, create a list where the element is zero if the corresponding row in Outcome
# is in the set bad_outcome; otherwise, it's one. Then assign it to the variable landing_class:
landing_class = [0 if i in bad_outcomes else 1 for i in df['Outcome']]
df['Class']=landing_class
df[['Class']].head(8)
# determine the success rate:
df["Class"].mean()
df.to_csv("dataset_part_2.csv", index=False)