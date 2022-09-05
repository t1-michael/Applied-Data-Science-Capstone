import requests
import pandas as pd
import numpy as np
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)


# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
        response = requests.get("https://api.spacexdata.com/v4/rockets/" + str(x)).json()
        BoosterVersion.append(response['name'])


# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        response = requests.get("https://api.spacexdata.com/v4/launchpads/" + str(x)).json()
        Longitude.append(response['longitude'])
        Latitude.append(response['latitude'])
        LaunchSite.append(response['name'])


# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
        response = requests.get("https://api.spacexdata.com/v4/payloads/" + load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])


# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/" + core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success']) + ' ' + str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])


spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print(response.content)

# Task 1: Request and parse the SpaceX launch data using the GET request
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response.status_code
# Use json_normalize meethod to convert the json result into a dataframe
data = pd.json_normalize(response.json())
data.head()
# We will now use the API again to get information about the launches using the IDs given for each launch.
# Specifically we will be using columns rocket, payloads, launchpad, and cores.

# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# From the rocket we would like to learn the booster name
# From the payload we would like to learn the mass of the payload and the orbit that it is going to
# From the launchpad we would like to know the name of the launch site being used, the longitude, and the latitude.
# From cores we would like to learn the outcome of the landing, the type of the landing, number of flights with that core,
# whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used,
# the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused,
# and the serial of the core. The data from these requests will be stored in lists and will be used to create a new dataframe.

# Global variables
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Now, let's apply  getBoosterVersion function method to get the booster version
getBoosterVersion()
BoosterVersion[0:5]
# Call getLaunchSite
getLaunchSite(data)
getPayloadData()
getCoreData()
# Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.
launch_dict = {'FlightNumber': list(data['flight_number']),
               'Date': list(data['date']),
               'BoosterVersion': BoosterVersion,
               'PayloadMass': PayloadMass,
               'Orbit': Orbit,
               'LaunchSite': LaunchSite,
               'Outcome': Outcome,
               'Flights': Flights,
               'GridFins': GridFins,
               'Reused': Reused,
               'Legs': Legs,
               'LandingPad': LandingPad,
               'Block': Block,
               'ReusedCount': ReusedCount,
               'Serial': Serial,
               'Longitude': Longitude,
               'Latitude': Latitude}
# Create a data from launch_dict
df = pd.DataFrame.from_dict(launch_dict)
df.head()

# Task 2: Filter the dataframe to only include Falcon 9 launches
# Hint data['BoosterVersion']!='Falcon 1'
data_falcon9 = df[df['BoosterVersion'] != 'Falcon 1']

# Now that we have removed some values we should reset the FlgihtNumber column
data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))
data_falcon9

# Data Wrangling
# We can see below that some of the rows are missing values in our dataset.
data_falcon9.isnull().sum()
# Task 3: Dealing with Missing Values
# Calculate below the mean for the PayloadMass using the .mean().
# Then use the mean and the .replace() function to replace np.nan values in the data with the mean you calculated.

# Calculate the mean value of PayloadMass column
payloadmassavg = data_falcon9['PayloadMass'].mean()
# Replace the np.nan values with its mean value
data_falcon9['PayloadMass'].replace(np.nan, payloadmassavg, inplace=True)

# To export the file in to a CSV format
data_falcon9.to_csv('dataset_part_1.csv', index=False)
