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
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('Please select a city from the list : "Washington", "New York City", "Chicago" : ').strip().lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city=input("\nPlease try again, that is not a city from the provided list").strip().lower()
    print("OK, City {} will be analyzed below! \n".format(city).title())


    # get user input for month (all, january, february, ... , june)
    month=input('Please specify a month (if needed), or choose "ALL" : "January", "February", "March", "April", "May", "June", "ALL" : ').strip().lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month=input("Please try again, there is no data for this month or the input was incorrect ").strip().lower()
    print("Thank you, the Month filter was set to {}! \n".format(month).title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Please specify a day (if needed), or choose "ALL" : "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "ALL" : ').strip().lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day=input("Please try again, something in the input was incorrect ").strip().lower()
    print("Thank you, the Day filter was set to {}! \n".format(day).title())

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)


    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular day of week:', popular_day_of_week)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station_sta = df['Start Station'].mode()[0]
    print('\nMost Common Start station:\n', popular_station_sta)

    # display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    print('\nMost Common End station:\n', popular_station_end)

    # display most frequent combination of start station and end station trip
    df['Combination_sta_end'] ="FROM: " + df['Start Station'] +"   TO: "+ df['End Station']
    popular_combination_sta_end = df['Combination_sta_end'].mode()[0]
    print('\nMost Frequent Trip (combination of start and end station):\n', popular_combination_sta_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\nTotal trip duration was \n", time.strftime("%j:%H:%M:%S", time.gmtime(df['Trip Duration'].sum())))
    # display mean travel time
    print("\nAvarage trip duration was \n", time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].mean())))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nReport for the user types is below")
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    print("\nReport for the Gender types is below")
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    except Exception as exception_gender:
        print("\nSorry, We could not generate this report, no such data input was found: {} \n" .format(exception_gender))

    # Display earliest, most recent, and most common year of birth
    print("\nReport for the Birth Years is below")
    try:
        min_birth_year = df['Birth Year'].min()
        print("The Earliest Birth Year is : ", min_birth_year)
        max_birth_year = df['Birth Year'].max()
        print("The Most Recent Birth Year is : ", max_birth_year)
        popular_birth_year = df['Birth Year'].mode()[0]
        print("The Most common Birth Year is : ", popular_birth_year)
    except Exception as exception_year:
        print("\nSorry, We could not generate this report, no such data input was found: {} \n".format(exception_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_decision(df):

    """Displays raw data upon request.
            Function prompts the user if they want to see 5 lines of raw data,
            displays the data if the answer is 'yes' and continue with the prompts
            and displays until the user says 'no' or something else, which is not 'yes'"""

    raw_decision = input("\nWould you like to see 5 lines of RAW data, type yes or no?\n").strip().lower()
    while raw_decision.lower() != 'no':
        start_point=0
        end_point=5
        cont ="yes"
        while cont == "yes":
            print(df.iloc[start_point:end_point,:])
            cont = input(" Shall we continue, do you want to see the next fiive rows? Enter - yes or no?")
            start_point+=5
            end_point+=5
            if cont != "yes":
                raw_decision = "no"
    print('-'*40)
    print("Thank you, that was the end of the RAW DATA report\n")



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_decision(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
