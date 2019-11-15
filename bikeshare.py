import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months_lst = ['january', 'february', 'march', 'april', 'may', 'june']
city = ''


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
    global city
    while city not in {'chicago', 'new york city', 'washington'}:
        try:
            city = str(input('\nChoose a city: chicago, new york city or washington\n'))
        except KeyboardInterrupt:
            continue

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in {'all', 'january', 'february', 'march', 'april', 'may', 'june'}:
        try:
            month = str(input('\nChoose a month: all, january, february, march, april, may or june\n'))
        except KeyboardInterrupt:
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        try:
            day = str(input('\nChoose a day: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday\n'))
        except KeyboardInterrupt:
            continue

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_int = months_lst.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_int]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].unique().size == 1:
        month = months_lst[int(df['month'].unique()[0]) - 1]
        print('\nYou\'ve filtered on: ' + month.title() + '.')
    else:
        popular_month = months_lst[int(df['month'].mode()[0]) - 1]
        print('\nThe most common month of travel is: ' + popular_month.title() + '.')

    # display the most common day of week
    if df['day_of_week'].unique().size == 1:
        weekday = df['day_of_week'].unique()[0]
        print('\nYou\'ve filtered on: ' + weekday + '.')
    else:
        popular_weekday = df['day_of_week'].mode()[0]
        print('\nThe most common day of week of travel is: ' + popular_weekday + '.')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common hour of day of travel is: ' + str(popular_hour) + 'h00.')
    print("\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().index[0]
    print('\nThe most popular start station is: ' + popular_start_station + '.')

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().index[0]
    print('\nThe most popular end station is: ' + popular_end_station + '.')

    # display most frequent combination of start station and end station trip
    df['Station combination'] = df['Start Station'] + ' - ' + df['End Station']
    popular_combination = df['Station combination'].value_counts().index[0]
    print('\nThe most popular combination of stations is: ' + popular_combination + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe total travel time is: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('\nThe counts for each user type are:\n')
    print(user_types_count)

    # Display counts of gender
    if city == 'washington':
        print('\nThere are no gender stats for Washington.')
    else:
        gender_count = df['Gender'].value_counts()
        print('\nThe counts for each gender are:\n')
        print(gender_count)

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nThere are no year of birth stats for Washington.')
    else:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        popular_birth = int(df['Birth Year'].mode()[0])
        print('\nThe earliest birth year is: ' + str(earliest_birth) + '.')
        print('\nThe most recent birth year is: ' + str(most_recent_birth) + '.')
        print('\nThe most common birth year is: ' + str(popular_birth) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    while True:
        see_raw_data = ''
        see_raw_data = str(input('\nDo you want to see the raw data? Enter yes or no.\n'))
        if see_raw_data == 'yes':
            print(df.head())
            df = df.drop(df.head().index)
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
