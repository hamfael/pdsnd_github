import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("From which city do you like to see data? Choose between Chicago, New York or Washington\n").title()
        if city == 'Chicago' or city == 'Washington' or city == 'New York':
            break
        else:
            print("Wrong city name, please input a valid city\n")

    # get user input for month (all, january, february, ... , june)
    # creating a list with month names to check valid inputs
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('\nTo filter data by month, please specify a month or type "all" for no month filter (Note that only first 6 months are available)\n').lower()
        if month in months:
            break
        elif month == 'all':
            break
        else:
            print('Wrong month name, please input a valid month name or "all"\n')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    # creating a list with the names of the days of week to check valid inputs
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while True:
        day = input('\nTo filter by day of week, please specify a day (monday, tuesday...) or type "all" for no day of week filter\n').lower()
        if day in days:
            break
        elif day == 'all':
            break
        else:
            print('Wrong day name, please input a valid day of week or "all"\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # reading data as received inputMon
    if city == 'Chicago':
        df = pd.read_csv('chicago.csv')
    elif city == 'New York':
        df = pd.read_csv('new_york_city.csv')
    else:
        df = pd.read_csv('washington.csv')

    # converting the start time column to datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of week, creating a new column to use as filter
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filtering by month
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filtering by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data(df):
    """Displays raw data to the user"""
    # set max columns to display to 200
    pd.set_option('display.max_columns',200)

    while True: # while loop and if statement to check valid input
        raw = input("\nWould you like to see the raw data? (Yes or No)\n").lower()
        if raw == 'yes':
            nrow = df.shape[0] # collecting number of rows
            #setting up the while loop to ask for the user 5 more lines
            i = 0
            j = 5
            while j <= nrow:
                print(df.iloc[i:j], "\n\n") #print 5 lines of the filtered data frame
                if j <= nrow:
                    next5 = input('Would you like to see the next 5 lines? (Yes or No)\n').lower()
                    if next5 == 'yes':
                        i = j
                        j += 5
                    else:
                        break
                else:
                    break
            break
        elif raw == 'no':
            break
        else:
            print("Please type Yes or No.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    com_month = df['month'].mode()[0]
    print('The most common month is:', com_month, '\n\n')

    # display the most common day of week
    com_dow = df['day_of_week'].mode()[0]
    print('The most common day of the week is:', com_dow, '\n\n')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_start_hour = df['hour'].mode()[0]
    print('The most common trip start hour is: {}h'.format(com_start_hour))

    print("\nThis took {} seconds.".format(round((time.time() - start_time), 3)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_start_station = df['Start Station'].mode()[0]
    com_start_station_value = df['Start Station'].value_counts().max()
    print('The most popular Start Station is {}, with {} trips.\n\n'.format(com_start_station, com_start_station_value))

    # display most commonly used end station
    com_end_station = df['End Station'].mode()[0]
    com_end_station_value = df['End Station'].value_counts().max()
    print('The most popular End Station is {}, with {} trips.\n\n'.format(com_end_station, com_end_station_value))

    # display most frequent combination of start station and end station trip
    com_start_end = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    com_start_end_value = (df['Start Station'] + df['End Station']).value_counts().max()
    print('The most popular "Start-End" combination of Stations is {}, with {} trips.\n'.format(com_start_end, com_start_end_value))

    print("\nThis calculation took {} seconds to run.".format(round((time.time() - start_time), 3)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_hours = round(total_time / 3600, 4)
    total_time_hour = total_time // 3600
    total_time_min = (total_time % 3600)
    total_time_sec = (total_time_min % 60)
    print('Total travel time is {} hours\nor'.format(total_time_hours))
    print('{} hours, {} minutes and {} seconds\n\n'.format(total_time_hour, total_time_min, total_time_sec))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_min = round(mean_travel_time // 60)
    mean_travel_time_sec = round(mean_travel_time % 60)
    print('The mean travel time is {} minutes and {} seconds\n'.format(mean_travel_time_min, mean_travel_time_sec))

    print("\nThis calculation took {} seconds to run".format(round((time.time() - start_time), 3)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The number of users by type is:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('\nThe number of users by gender is:\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nThe oldest user was born in {}\n'.format(round(df['Birth Year'].min())))
        print('The youngest user was born in {}\n'.format(round(df['Birth Year'].max())))
        print('The most common birth year between users is {}\n'.format(round(df['Birth Year'].mode()[0])))


    print("\nThis calculation took {} seconds to run".format(round((time.time() - start_time), 3)))
    print('-'*40)


def main():
    restart = 'yes'
    while restart == 'yes':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart == 'yes':
                break
            elif restart == 'no':
                break
            else:
                print('Please enter a valid input.')

if __name__ == "__main__":
	main()
