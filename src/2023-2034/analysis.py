import pandas as pd

csv_file = "newNbaSeason.csv"

# Read the CSV data into a pandas DataFrame
df = pd.read_csv(csv_file)

# # Convert the 'Date' column to datetime format
# df["Date"] = pd.to_datetime(df["Date"], format="%a %b %d %Y")

# # Sort the DataFrame based on the 'Date' column
# df = df.sort_values(by="Date")


def is_less_than_40_hours_apart(date1, date2):
    # 40 hours in seconds
    return abs((date1 - date2).total_seconds()) < (40 * 3600)


def get_rows_for_visitor(df, visitor_name):
    # Convert the 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], format="%a %b %d %Y")

    # Sort the DataFrame based on the 'Date' column
    df = df.sort_values(by="Date")

    # Initialize a list to store rows for the specified visitor
    rows_for_visitor = []
    df_len = len(df)
    # Iterate through the DataFrame
    for i in range(df_len):
        current_visitor = df["Visitor"].iloc[i]
        # current_home = df["Home"].iloc[i]
        current_date = df["Date"].iloc[i]
        # previous_visitor = df["Visitor"].iloc[i - 1]

        # if i + 1 == df_len:
        #     break

        # next_date = df["Date"].iloc[i + 1]

        # Check if the current row and the previous row belong to the specified visitor
        if current_visitor == visitor_name:  # or current_home == visitor_name
            # and previous_visitor == visitor_name:
            # Check if the dates are less than 40 hours apart
            # if is_less_than_40_hours_apart(current_date, previous_date):
            # Append the rows to the list
            # rows_for_visitor.append(df.iloc[i - 1])
            rows_for_visitor.append(df.iloc[i])

    # Create a new DataFrame from the list of rows
    result_df = pd.DataFrame(rows_for_visitor)

    return result_df


def get_consecutive_games_for_team(df):
    result_row = []
    for i in range(len(df)):
        # current_home = df["Home"].iloc[i]
        current_date = df["Date"].iloc[i]

        if i + 1 >= len(df):
            break

        next_date = df["Date"].iloc[i + 1]

        if is_less_than_40_hours_apart(current_date, next_date):
            result_row.append(df.iloc[i])
            result_row.append(df.iloc[i + 1])

    result_df = pd.DataFrame(result_row)

    return result_df


def get_teams(df):
    result_row = set()

    for i in range(len(df)):
        result_row.add(df["Visitor"].iloc[i])

    return result_row


df = pd.read_csv(csv_file)

teams = get_teams(df)
result_dict = {}
for team in teams:
    visitor_name = team
    result = get_rows_for_visitor(df, visitor_name)
    cre = get_consecutive_games_for_team(result)
    # print(cre)
    if cre.shape[0] % 2 != 0:
        raise ("Bad calculation")
    result_dict[team] = cre.shape[0] // 2

for key, value in sorted(result_dict.items(), key=lambda x: x[1]):
    print(key, value)
