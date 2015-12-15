import pandas as pd
from keen.client import KeenClient
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
from math import ceil

style.use('bmh')

# API Keys for EnhatchMarketingApp2.0
client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)


# Takes in a raw input of what the user wants to do
def user_wants():
    x = 1
    global decision1
    while x == 1:
        decision1 = input('What would you like to do today?\n'
                          '1) Find DAU\n'
                          '2) Find MAU\n'
                          '3) Find Both\n'
                          '4) Graph, or acquire information from previous pull\n')
        if decision1 == "1":  # if DAU is chosen, request the end date and then find DAU
            end_date_query()
            app_data_daily(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "2":  # if MAU is chosen, request the end date and then find MAU
            end_date_query()
            app_data_monthly(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "3":  # if both is chosen, request the end date and then find both
            end_date_query()
            app_data_daily(month=end_month, day=end_day, year=end_year)
            app_data_monthly(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "4":  # Use previous pull's data
            decision1 = input('\nWhat information did you use on the last pull?\n'
                              '1) DAU\n'
                              '2) MAU\n'
                              '3) Both\n')
            x = 2

        else:  # Error checking
            print("Wasn't a viable option, please pick again\n")
    python_graph()  # Creates the Python Graph
    data_end_use()  # Takes in a raw input of what the user wants to do with data acquried


def data_end_use():
    x = 1
    y = 1
    global decision1
    #
    try:
        if decision1 == '1':
            print('Handling DAU\n'
                  '____________________')
        elif decision1 == '2':
            print('Handling MAU\n'
                  '____________________')
        else:
            print('Handling both DAU and MAU\n'
                  '____________________________')
    except NameError:
        while y == 1:
            decision1 = input('What files are we handling?\n'
                              '1) DAU\n'
                              '2) MAU\n'
                              '3) Both')
            if decision1 == '1':
                y = 2
            elif decision1 != '2':
                y = 2
            elif decision1 != '3':
                y = 2
            else:
                print('Not a valid option, please try again')

    while x == 1:
        decision2 = input('What would you like to do with the information acquired?\n'
                          '1) Dump into a csv\n'
                          '2) Dump into a JSON\n'
                          '3) Create a Plotly graph\n'
                          '4) Nothing\n')
        if decision2 == '1':
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.to_csv('DAU.csv')
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.to_csv('MAU.csv')
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.to_csv('MAU_DAU.csv')
            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '2':
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.to_json('DAU.json')
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.to_json('MAU.json')
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.to_json('MAU_DAU.json')
            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '3':
            graph_name = input('\nWhat would you like to name the graph?\n')
            graph_folder = input('\nWhat folder would you like to put the graph in?\n')
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.iplot(kind='scatter', filename=graph_folder + graph_name)
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.iplot(kind='scatter', filename=graph_folder + graph_name)
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name)
            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '4':
            break

        else:
            print("That wasn't a viable option, please try again")


def python_graph():
    if decision1 == '1':
        dau_df = pd.read_pickle('DAU.pickle')
        dau_df['DAU'].plot()
        plt.legend(loc='best')
        plt.title('DAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif decision1 == '2':
        mau_df = pd.read_pickle('MAU.pickle')
        mau_df['MAU'].plot()
        plt.legend(loc='best')
        plt.title('MAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif decision1 == '3':
        mau_df = pd.read_pickle('MAU.pickle')
        dau_df = pd.read_pickle('DAU.pickle')
        mau_dau_df = dau_df.join(mau_df)

        division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
        df = pd.DataFrame(division)
        df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
        main_df = mau_dau_df.join(df)
        main_df.plot(secondary_y=['DAU/MAU %'])
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()


def end_date_query():
    x = 1
    while x == 1:
        print('Specify query end date\n-------------------------')
        global end_month
        global end_day
        global end_year
        try:
            end_date_raw = input("\nWhat date would you like the query to end?\n"
                                 "Please put it in format MM/DD/YYYY:\n")
            end_day = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%d'))
            end_month = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%m'))
            end_year = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%Y'))
            x = 2
        except ValueError:
            print("That was incorrect format, please try again\n")

    x = 1
    while x == 1:
        question = input("\nWould you like to:\n"
                         "1)Go a set number of days back?\n"
                         "2)Pick a specific date in the past to start?\n"
                         "1 or 2?:")
        if question == '1':
            global query_size
            query_size = int(input("\nHow many days do you want in this query?")) + 1
            x = 2
        elif question == '2':
            start_date_raw = input("\nWhat date would you like the query to start?\n"
                                   "Please put it in format MM/DD/YYYY:\n")
            try:
                start_day = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%d'))
                start_month = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%m'))
                start_year = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%Y'))
                d1 = dt.datetime(end_year, end_month, end_day)
                d2 = dt.datetime(start_year, start_month, start_day)
                query_size = abs((d1-d2).days + 1)
                x = 2
            except ValueError:
                print("that was incorrect format, please try again\n")
        else:
            print("That wasn't a viable option, please try again and pick 1 or 2")
    x = 1
    while x == 1:
        question2 = input("\nWould you like to exclude weekends?\nY = 1/N = 2?:")
        global weekends
        if question2 == "Y" or question2 == "y" or question2 == "1":
            weekends = False
            x = 2
        elif question2 == "N" or question2 == "n" or question2 == "2":
            weekends = True
            x = 2
        else:
            print("Not a viable option, please try again")


def daily_query_start(day, month, year):
    start_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(dt.datetime(year, month, (day+1)).date()), 'start': str(start_day.date())}
    return query


def monthly_query_start(day, month, year):
    monthly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size + 30)
    monthly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(monthly_end_day), 'start': str(monthly_start_day)}
    return query


def extract_date_daily(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['start'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


def extract_date_monthly(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['end'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


def app_data_daily(month, day, year):
    if not weekends:
        start_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
        num_weeks = ceil(query_size / 7)
        if query_size % 7 == 0:
            num_weeks += 1
        week_day = start_day.weekday()
        if week_day == 5:
            day_of_week = start_day + dt.timedelta(2)
        elif week_day == 6:
            day_of_week = start_day + dt.timedelta(1)
        else:
            day_of_week = start_day
        query = []

        while num_weeks != 1:
            next_day1 = day_of_week + dt.timedelta(1)
            if next_day1.weekday() == 5:
                query_part = {'end': str(next_day1), 'start': str(day_of_week)}
                day_of_week = next_day1 + dt.timedelta(2)
            else:
                next_day2 = next_day1 + dt.timedelta(1)
                if next_day2.weekday() == 5:
                    query_part = {'end': str(next_day2), 'start': str(day_of_week)}
                    day_of_week = next_day2 + dt.timedelta(2)
                else:
                    next_day3 = next_day2 + dt.timedelta(1)
                    if next_day3.weekday() == 5:
                        query_part = {'end': str(next_day3), 'start': str(day_of_week)}
                        day_of_week = next_day3 + dt.timedelta(2)
                    else:
                        next_day4 = next_day3 + dt.timedelta(1)
                        if next_day4.weekday() == 5:
                            query_part = {'end': str(next_day4), 'start': str(day_of_week)}
                            day_of_week = next_day4 + dt.timedelta(2)
                        else:
                            next_day5 = next_day4 + dt.timedelta(1)
                            query_part = {'end': str(next_day5), 'start': str(day_of_week)}
                            day_of_week = next_day5 + dt.timedelta(2)
            query.append(query_part)
            num_weeks -= 1

        if day_of_week == dt.datetime(year, month, day):
            next_day1 = day_of_week + dt.timedelta(1)
            query_part = {'end': str(next_day1), 'start': str(day_of_week)}
        else:
            next_day1 = day_of_week + dt.timedelta(1)
            if next_day1 == dt.datetime(year, month, day):
                next_day2 = next_day1 + dt.timedelta(1)
                query_part = {'end': str(next_day2), 'start': str(day_of_week)}
            else:
                next_day2 = next_day1 + dt.timedelta(1)
                if next_day2 == dt.datetime(year, month, day):
                    next_day3 = next_day2 + dt.timedelta(1)
                    query_part = {'end': str(next_day3), 'start': str(day_of_week)}
                else:
                    next_day3 = next_day2 + dt.timedelta(1)
                    if next_day3 == dt.datetime(year, month, day):
                        next_day4 = next_day3 + dt.timedelta(1)
                        query_part = {'end': str(next_day4), 'start': str(day_of_week)}
                    else:
                        next_day4 = next_day3 + dt.timedelta(1)
                        next_day5 = next_day4 + dt.timedelta(1)
                        query_part = {'end': str(next_day5), 'start': str(day_of_week)}

        query.append(query_part)

        temp_df = pd.DataFrame()
        for item in query:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=item,
                                           timezone=5,
                                           interval='daily')
            extract_date_daily(app_data)
            df = pd.DataFrame(app_data)
            if temp_df.empty:
                temp_df = pd.DataFrame(app_data)
            else:
                temp_df = temp_df.merge(df, how='outer')
    else:
        temp_df = pd.DataFrame()
        app_data = client.count_unique('Page', 'user.pk',
                                       timeframe=daily_query_start(day, month, year),
                                       timezone=5,
                                       interval='daily')
        extract_date_daily(app_data)
        df = pd.DataFrame(app_data)
        if temp_df.empty:
            temp_df = pd.DataFrame(app_data)
        else:
            temp_df = temp_df.merge(df, how='outer')

    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'DAU'}, inplace=True)
    temp_df.to_pickle('DAU.pickle')
    print(temp_df)


def app_data_monthly(month, day, year):
    x = 0
    day1 = day
    month1 = month
    year1 = year
    temp_df = pd.DataFrame
    while x < query_size:
        if not weekends:
            if (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 5 or \
               (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 6:
                new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
                day1 = int(new_date.strftime('%d'))
                month1 = int(new_date.strftime('%m'))
                year1 = int(new_date.strftime('%Y'))
                x += 1
                continue
            else:
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=monthly_query_start(day1, month1, year1),
                                               timezone=5)
                list_dict = [{'Date': str((dt.datetime(year1, month1, day1) -
                                           dt.timedelta(query_size-1)).strftime('%m-%d-%Y')),
                              'value': app_data}]
                df = pd.DataFrame(list_dict)

                if temp_df.empty:
                    temp_df = df
                else:
                    temp_df = temp_df.merge(df, how='outer')
                x += 1
                new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
                day1 = int(new_date.strftime('%d'))
                month1 = int(new_date.strftime('%m'))
                year1 = int(new_date.strftime('%Y'))
        else:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=monthly_query_start(day1, month1, year1),
                                           timezone=5)
            list_dict = [{'Date': str((dt.datetime(year1, month1, day1) -
                                       dt.timedelta(query_size-1)).strftime('%m-%d-%Y')),
                          'value': app_data}]
            df = pd.DataFrame(list_dict)

            if temp_df.empty:
                temp_df = df
            else:
                temp_df = temp_df.merge(df, how='outer')
            x += 1
            new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
            day1 = int(new_date.strftime('%d'))
            month1 = int(new_date.strftime('%m'))
            year1 = int(new_date.strftime('%Y'))

    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'MAU'}, inplace=True)
    temp_df.to_pickle('MAU.pickle')
    print(temp_df)

user_wants()
