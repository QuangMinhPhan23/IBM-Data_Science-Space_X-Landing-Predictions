# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
import requests

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df = pd.read_csv(URL)

# We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch.
# We see that as the flight number increases, the first stage is more likely to land successfully.
# The payload mass also appears to be a factor; even with more massive payloads, the first stage 
# often returns successfully.
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# TASK 1: Visualize the relationship between Flight Number and Launch Site
# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site,
# and hue to be the class value
plt.figure(figsize=(16, 8))
sns.catplot(x='FlightNumber', y='LaunchSite', hue='Class', data=df)
plt.xlabel('Flight Number', fontsize=20)
plt.ylabel('Launch Site', fontsize=20)
plt.show()

# TASK 2: Visualize the relationship between Payload Mass and Launch Site
# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site,
# and hue to be the class value
plt.figure(figsize=(16, 8))
sns.catplot(x='PayloadMass', y='LaunchSite', hue='Class', data=df)
plt.xlabel('Payload Mass (kg)', fontsize=20)
plt.ylabel('Launch Site', fontsize=20)
plt.show()

# TASK 3: Visualize the relationship between success rate of each orbit type
# Plot a bar chart of Orbit and the success rate
df_orbit = df.groupby(['Orbit', 'Class']).size().unstack()
df_orbit.plot(kind='bar', stacked=True, figsize=(16, 8))
plt.xlabel('Orbit', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.show()

# TASK 4: Visualize the relationship between FlightNumber and Orbit type
# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit,
plt.figure(figsize=(16, 8))
sns.catplot(x='FlightNumber', y='Orbit', data=df)
plt.xlabel('Flight Number', fontsize=20)
plt.ylabel('Orbit', fontsize=20)
plt.show()

# TASK 5: Visualize the relationship between Payload and Orbit type
# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit,
plt.figure(figsize=(16, 8))
sns.catplot(x='PayloadMass', y='Orbit', data=df)
plt.xlabel('Payload Mass (kg)', fontsize=20)
plt.ylabel('Orbit', fontsize=20)
plt.show()

# TASK 6: Visualize the launch success yearly trend
# Plot a line chart with x axis to be the year and y axis to be the success rate,
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()
df_year = df.groupby(['Date', 'Class']).size().unstack()
df_year.plot(kind='line', figsize=(16, 8))
plt.xlabel('Year', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.show()

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

# TASK 7: Create dummy variables to categorical columns
# Use the function get_dummies and features dataframe to apply OneHotEncoder to the column Orbits,
# LaunchSite, LandingPad, and Serial. Assign the value to the variable features_one_hot,
# display the results using the method head
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
print(features_one_hot.describe())

# TASK 8: Cast all numeric columns to float64
# Cast all numeric columns to float64 using astype method
features_one_hot = features_one_hot.astype('float64')
features_one_hot.to_csv('dataset_part_3.csv', index=False)