import matplotlib.pyplot as plt
import csv
from typing import List
from numpy import arange

# set the data location folder
files_path = "./python_data_visualization/data"

# file names with corresponding data settings
file_names = ["rsel.csv", "cel-rs.csv", "2cel-rs.csv", "cel.csv", "2cel.csv"] 
legend_names = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
data_colors = ["blue", "green", "red", "black", "magenta"]

def read_file(file_name: str) -> List[float]:
    with open(f"{files_path}/{file_name}") as csvfile: 
        data_reader = csv.reader(csvfile, delimiter = ',')
        header = next(data_reader) # read the header line

        data = []
        for row in data_reader:
            # read the average value for each of the runs
            # multiply for better visualization
            avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:]))) * 100 
            data.append(avg)

        return data

def draw_plot(combined_data: List[List[float]]) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(6, 6))

    # add data to the first subplot
    for i, data in enumerate(combined_data):
        axs[0].plot(data, label=legend_names[i], linewidth=0.8, color=data_colors[i])

    # add data to the second subplot
    axs[1].plot(data)

    # apply common changes
    for ax in axs:
        ax.set_ylim(60, 100)
        ax.set_yticks(arange(60, 101, 5)) # make sure the tick step is 5
        ax.tick_params(direction='in') # draw the tick marks inside the subplot

    #
    # changes to the first subplot
    #
    # TODO: configure the grid to match the result
    axs[0].grid(which='both', linestyle='dotted', linewidth=0.8, color='gray') 
    axs[0].set_title("Pokolenie")
    axs[0].set_ylabel("Odsetek wygranych gier [%]")
    axs[0].legend(loc="lower right")
    # configure the x axis 
    axs[0].xaxis.tick_top() 
    axs[0].set_xlim(0, 200)
    axs[0].set_xticks(arange(0, 201, 40))
    # create the secondary axis and scale it accordingly
    secax = axs[0].secondary_xaxis("bottom", functions=(lambda x: x * 2.5, lambda x: x / 2.5)) 
    secax.tick_params(axis='x', direction='in') # set the axis's tick marks location
    secax.set_xlabel("Rozegranych gier (×1000)")

    #
    # changes to the second subplot
    #
    axs[1].yaxis.tick_right()

    plt.show()


def main() -> None:
    # set the font properties
    plt.rcParams['font.size'] = 9

    # TODO: Decide on the font sizes
    # plt.rcParams['axes.titlesize'] = 16  # Font size for axis titles
    # plt.rcParams['axes.labelsize'] = 14  # Font size for axis labels
    # plt.rcParams['xtick.labelsize'] = 12  # Font size for x-axis tick labels
    # plt.rcParams['ytick.labelsize'] = 12  # Font size for y-axis tick labels

    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'

    # read the data
    combined_data = []
    for name in file_names:
        combined_data.append(read_file(name))
    
    draw_plot(combined_data);


if __name__ == "__main__":
    main()