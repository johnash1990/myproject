"""pronto_utils.py"""

import wget
import os
import zipfile
import pandas as pd

import matplotlib.pyplot as plt
import seaborn; seaborn.set()  # for plot stylings

# added for HW_4
import urllib3
import certifi
import sys


def download_if_needed(URL, filename):
    """
    Download from URL to filename unless filename already exists
    This function was modified beyond the version shown in class
    to use the urllib3 module instead of zipfile
    """

    if os.path.exists(filename):
        print(filename, 'already exists')
        return
    else:
        print('downloading', filename)

        # needed for https
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', # Force certificate check.
            ca_certs=certifi.where(),  # Path to the Certifi bundle.
            retries=3
        )

        try:
            response = http.request('GET',URL)
            with open(filename,'wb') as f:
                f.write(response.data)
            f.close()
            response.release_conn()
        # keep the exception handling general since many types of
        # exceptions are possible
        except:
            e = sys.exc_info()[0]
            print('Error! Data not downloaded.',e)

"""
This is the old version of this function as developed in class
Comment it out for now
"""
# def download_if_needed(URL, filename):
#     """
#     Download from URL to filename unless filename already exists
#     """
#     if os.path.exists(filename):
#         print(filename, 'already exists')
#         return
#     else:
#         print('downloading', filename)
#         wget.download(URL)

def get_pronto_data():
    """
    Download pronto data, unless already downloaded
    """
    download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip',
                       'open_data_year_one.zip')


def get_trip_data():
    """
    Fetch pronto data (if needed) and extract trips as dataframe
    """
    get_pronto_data()
    zf = zipfile.ZipFile('open_data_year_one.zip')
    file_handle = zf.open('2015_trip_data.csv')
    return pd.read_csv(file_handle)


def get_weather_data():
    """
    Fetch pronto data (if needed) and extract weather as dataframe
    """
    get_pronto_data()
    zf = zipfile.ZipFile('open_data_year_one.zip')
    file_handle = zf.open('2015_weather_data.csv')
    return pd.read_csv(file_handle)


def get_trips_and_weather():
    trips = get_trip_data()
    weather = get_weather_data()

    # This is a nice way to access date info in a column
    date = pd.DatetimeIndex(trips['starttime'])

    # pivot table = two-dimensional groupby
    trips_by_date = trips.pivot_table('trip_id', aggfunc='count',
                                      index=date.date, columns='usertype')

    weather = weather.set_index('Date')
    weather.index = pd.DatetimeIndex(weather.index)
    weather = weather.iloc[:-1]
    return weather.join(trips_by_date)


def plot_daily_totals():
    data = get_trips_and_weather()
    fig, ax = plt.subplots(2, figsize=(14, 6), sharex=True)
    data['Annual Member'].plot(ax=ax[0], title='Annual Member')
    data['Short-Term Pass Holder'].plot(ax=ax[1], title='Short-Term Pass Holder')
    fig.savefig('daily_totals.png')

def remove_data():
    """
    ADDED FOR HW_4
    Removes zip file containing the Pronto data as well as any other
    cached data (such as the .csv or readme files if the file was unzipped)
    """

    # get the current working directory
    cwd = os.getcwd()

    # construct the file path of the zip file by appending the filename to the cwd
    zipData = cwd + '\open_data_year_one.zip'

    # file paths of individual csv files and readme
    stationData = cwd + '\\2015_station_data.csv'
    statusData = cwd + '\\2015_status_data.csv'
    tripData = cwd + '\\2015_trip_data.csv'
    weatherData = cwd + '\\2015_weather_data.csv'
    README = cwd + '\README.txt'

    # check if the files exist, and if so, delete them
    if os.path.exists(zipData):
        os.remove(zipData)

    if os.path.exists(stationData):
        os.remove(stationData)

    if os.path.exists(statusData):
        os.remove(statusData)

    if os.path.exists(tripData):
        os.remove(tripData)

    if os.path.exists(weatherData):
        os.remove(weatherData)

    if os.path.exists(README):
        os.remove(README)

    # alert the user the operations have completed
    print('All possibly existing cached data, including the zip file, has been removed')
