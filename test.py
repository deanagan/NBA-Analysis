from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

filename = 'NBASchedule.csv'


# data=pd.read_csv(filename)
df = pd.read_csv(filename)

unique_teams = df["Home/Neutral"].unique()

# print(unique_teams)
# print(len(unique_teams))

team_num_road_b2bs = {}
for team in unique_teams:
    # if team != 'Phoenix Suns':
    #     continue
    # matching_rows = df.loc[(df["Visitor/Neutral"] == team) | (df["Home/Neutral"] == team)].copy()
    matching_rows = df.loc[(df["Visitor/Neutral"] == team)].copy()

    matching_rows['DateTimeStr'] = matching_rows['Date'].str.cat(matching_rows['Start (ET)'], sep= " ")
    matching_rows['DateTimeStr'] = matching_rows['DateTimeStr'].str[:-1]
    matching_rows['DateTime'] = pd.to_datetime(matching_rows['DateTimeStr'], format='%a %b %d %Y %I:%M')
    matching_rows['HourDiff'] = (matching_rows['DateTime'] - matching_rows['DateTime'].shift()).dt.total_seconds()/3600
    matching_rows["HourDiffToNext"] = matching_rows["HourDiff"].shift(-1)

    # if team == 'Los Angeles Clippers':
    #     a = matching_rows[['DateTimeStr', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1', 'HourDiff' ]]
    #     print(len(a))
    #     print(a)


    # print(matching_rows[['DateTimeStr', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1', 'HourDiff' ]].head(n = 10))



    second_of_b2b = matching_rows.loc[matching_rows["HourDiff"] < 35.0]

    first_of_b2b = matching_rows.loc[matching_rows["HourDiffToNext"] < 35.0]


    result = pd.concat([first_of_b2b, second_of_b2b]).sort_values(by='DateTime')


    # for i in range(0, len(result), 2):
    #     print(result.iloc[i:i+2][['DateTimeStr', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1']])
    #     print()

    team_num_road_b2bs[team] = len(second_of_b2b)

print("Road back to back Summary:")
for team, total_road_b2bs in sorted(team_num_road_b2bs.items(), key=lambda item: item[1], reverse=True):
    print(team, total_road_b2bs)


teams = team_num_road_b2bs.keys()
print(teams)

# # Data for plotting
# x = [1, 2, 3, 4, 5]
# y = [10, 15, 13, 17, 20]

# # Create the figure and axes objects
# fig, ax = plt.subplots()

# # Plot the data
# ax.bar(x, y)

# # Add labels and title
# plt.xlabel('X-axis Label')
# plt.ylabel('Y-axis Label')
# plt.title('Bar Graph Title')

# # Show the plot
# plt.show()