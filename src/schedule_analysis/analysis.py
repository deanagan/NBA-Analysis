import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

year = '2022-23'
current_sub_path = "src/schedule_analysis"
csv_file = f"NBA-{year}-RegularSeason.csv"

team_name_gif = ['atlantahawks.gif', 'bostonceltics.gif', 'brooklynnets.gif', 'charlottehornets.gif', 'chicagobulls.gif', 'clevelandcavaliers.gif', 'dallasmavericks.gif', 'denvernuggets.gif', 'detroitpistons.gif', 'goldenstatewarriors.gif', 'houstonrockets.gif', 'indianapacers.gif', 'losangelesclippers.gif', 'losangeleslakers.gif', 'memphisgrizzlies.gif',
                 'miamiheat.gif', 'milwaukeebucks.gif', 'minnesotatimberwolves.gif', 'neworleanspelicans.gif', 'newyorkknicks.gif', 'oklahomacitythunder.gif', 'orlandomagic.gif', 'philadelphia76ers.gif', 'phoenixsuns.gif', 'portlandtrailblazers.gif', 'sacramentokings.gif', 'sanantoniospurs.gif', 'torontoraptors.gif', 'utahjazz.gif', 'washingtonwizards.gif']


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

        # Check if the current row and the previous row belong to the specified visitor
        if current_visitor == visitor_name:  # or current_home == visitor_name
            rows_for_visitor.append(df.iloc[i])

    return pd.DataFrame(rows_for_visitor)


def get_consecutive_games_for_team(df):
    result_row = []
    for i in range(len(df)):
        # current_home = df["Home"].iloc[i]
        current_date = df["Date"].iloc[i]

        if i + 1 >= len(df):
            break

        next_date = df["Date"].iloc[i + 1]

        if is_less_than_40_hours_apart(current_date, next_date):
            result_row.extend((df.iloc[i], df.iloc[i + 1]))

    return pd.DataFrame(result_row)


def get_teams(df):
    return {df["Visitor"].iloc[i] for i in range(len(df))}


def draw_chart(team_totals, season):

    x = list(team_totals.keys())
    num_games = list(team_totals.values())

    # Create the figure and axes objects
    fig, ax = plt.subplots()

    for i, team in enumerate(x):
        name = f"{team.lower().replace(' ', '')}.gif"
        gif_path = os.path.join(os.getcwd(), current_sub_path, name)
        y_axis_image = plt.imread(gif_path)

        # Define the position and size of the image
        imagebox = OffsetImage(y_axis_image, zoom=0.1, resample=True,
                               clip_path=None, clip_box=None, alpha=None)

        # Create a custom annotation box for the image
        ab = AnnotationBbox(imagebox, (0, i), frameon=False, pad=0)

        # Add the custom annotation box to the x-axis
        ax.add_artist(ab)

        # Annotate the bar with its value, add 0.2 so there is space from the tip of the bar to the number
        ax.text(team_totals[team] + 0.2, i, str(
            team_totals[team]), va='center', ha='left')

    # Set the size of the figure
    fig.set_size_inches(10, 8)

    # Plot the data
    # ax.bar(x, y)

    # Create a bar chart with the values
    ax.barh(np.arange(len(num_games)), num_games)

    # Set x-axis labels to an empty list since we're using images
    ax.set_yticklabels([])

    ax.set_xticks(np.arange(1, 11))

    # Remove borders except bottom
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Keep the vertical gridlines
    ax.xaxis.grid(True)

    # Add labels and title
    plt.xlabel('Number of Road Back-To-Backs')
    plt.ylabel('')
    plt.title(f'NBA {season} Season Total Road Back-to-Back Games')

    # Show the plot
    # plt.show()

    # Save the plot
    plt.savefig(f'{season}.png')


# Read the CSV data into a pandas DataFrame
df = pd.read_csv(os.path.join(os.getcwd(), current_sub_path, csv_file))


teams = get_teams(df)
result_dict = {}
for team in teams:
    visitor_name = team
    result = get_rows_for_visitor(df, visitor_name)
    cre = get_consecutive_games_for_team(result)
    # print(cre)
    if cre.shape[0] % 2 != 0:
        raise ValueError("Bad calculation")
    result_dict[team] = cre.shape[0] // 2

# top10 = (sorted(result_dict.items(), key=lambda x: x[1])[:10])
# bottom10 = (sorted(result_dict.items(),
#                    key=lambda x: x[1], reverse=True)[:10])

sorted_result_dict = dict(
    sorted(result_dict.items(), key=lambda x: (x[1], tuple(-ord(c) for c in x[0]))))  # break the tie and use alphabetical order

for key, value in sorted_result_dict.items():
    print(key, value)


draw_chart(sorted_result_dict, year)
