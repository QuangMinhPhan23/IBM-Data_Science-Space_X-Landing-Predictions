import csv, sqlite3


con = sqlite3.connect("my_data1.db")
cur = con.cursor()
import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

#DROP THE TABLE IF EXISTS
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
cur.execute("create table SPACEXTABLE as select * from SPACEXTBL where Date is not null")

# Display the names of the unique launch sites in the space mission
cur.execute("SELECT DISTINCT Launch_Site FROM SPACEXTABLE")
print(cur.fetchall())

# Task 2 Display 5 records where launch sites begin with the string 'CCA'
cur.execute("SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5")

# Display the total payload mass carried by boosters launched by NASA (CRS)
cur.execute("SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE CUSTOMER = 'NASA (CRS)'")

# Display average payload mass carried by booster version F9 v1.1
cur.execute("SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE BOOSTER_VERSION = 'F9 v1.1'")

# Display the date when the first successful landing outcome in ground pad was acheived.
cur.execute("SELECT MIN(Date) FROM SPACEXTABLE WHERE LANDING_OUTCOME = 'Success (ground pad)'")

# List the names of the boosters which have success in drone ship and have payload mass greater
# than 4000 but less than 6000
cur.execute("SELECT BOOSTER_VERSION FROM SPACEXTABLE WHERE LANDING_OUTCOME = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000")

# List the total number of successful and failure mission outcomes
cur.execute("SELECT COUNT(*) FROM SPACEXTABLE WHERE MISSION_OUTCOME = 'Success'")

# List the   names of the booster_versions which have carried the maximum payload mass. Use a subquery
cur.execute("SELECT BOOSTER_VERSION FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)")

# List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions,
# launch_site for the months in year 2015.
# Note: SQLLite does not support monthnames. So you need to use substr(Date, 6,2) as month to get the months 
# and substr(Date,0,5)='2015' for year.
cur.execute("SELECT SUBSTR(Date, 6, 2) AS Month, LANDING_OUTCOME, BOOSTER_VERSION, LAUNCH_SITE FROM SPACEXTABLE WHERE LANDING_OUTCOME = 'Failure (drone ship)' AND SUBSTR(Date, 0, 5) = '2015'")

# Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date
# 2010-06-04 and 2017-03-20,  in descending order.
cur.execute("SELECT LANDING_OUTCOME, COUNT(*) FROM SPACEXTABLE WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY LANDING_OUTCOME ORDER BY COUNT(*) DESC")
