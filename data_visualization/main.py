import matplotlib.pyplot as plt
from numpy import arange, transpose
from pandas import read_csv
from typing import List

# NOTE: SET THE FOLDER CONTAINING THE DATA FILES !
files_path = './data_visualization/data'

# file names with corresponding data settings
file_names = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv'] 
legend_names = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
data_colors = ['blue', 'green', 'red', 'black', 'magenta']
markers = ['o', 'v', 'D', 's', 'd']


def read_file(file_name: str) -> tuple[List[float], List[float]]:
    data_reader = read_csv(f'{files_path}/{file_name}', skiprows=1, header=None)

    data = []
    for _, row in data_reader.iterrows():
        # read the average value for each of the runs
        # multiply for better visualization
        avg = row[2:].mean() * 100
        data.append(avg)
    
    boxplot_data = (data_reader.iloc[-1, 2:] * 100).tolist()
    
    return(data, boxplot_data)


def draw_plot(combined_data: List[List[float]], boxplot_combined_data: List[List[float]]) -> None:
    # set the font properties
    plt.rcParams['font.size'] = 9.6
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams['axes.titlesize'] = 9.6
    plt.rcParams['legend.fontsize'] = 9.5
    # set the rest of the parameters
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.bottom'] = True
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.major.width'] = 0.7
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.right'] = True
    plt.rcParams['ytick.major.size'] = 3.7
    plt.rcParams['ytick.major.width'] = 0.7
    plt.rcParams['legend.edgecolor'] = 'gray'

    # define the size and number of subplots
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 5))

    # add data to the first subplot
    for i, data in enumerate(combined_data):
        axs[0].plot(data, markers[i], ls='-', label=legend_names[i], linewidth=0.85, 
        color=data_colors[i], markevery=25, markeredgecolor='black', markersize=5, markeredgewidth=0.5)

    # add data to the second subplot and change style of boxplot
    axs[1].boxplot(boxplot_combined_data, tick_labels=legend_names, notch=True, showmeans=True,
                   boxprops=dict(color='blue'),
                   flierprops=dict(marker='+', markeredgecolor='blue', markersize=6, markeredgewidth=0.7),
                   meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='blue', markersize=4),
                   medianprops=dict(color='red'),
                   capprops=dict(linewidth=0.85),
                   whiskerprops=dict(linestyle='--', linewidth=1, color='blue', dashes=(6, 5.5)))

    #
    # apply common changes
    #
    fig.canvas.manager.set_window_title('Data visualization')
    for ax in axs:
        ax.set_ylim(60, 100)
        ax.set_yticks(arange(60, 101, 5)) # make sure the tick step is 5

    #
    # changes to the first subplot
    #
    axs[0].grid(which='both', color='darkgray', dashes=(1.2, 3.6)) 
    axs[0].set_title('Pokolenie')
    axs[0].set_ylabel('Odsetek wygranych gier [%]')
    axs[0].legend(numpoints=2, handlelength=2, loc='lower right', framealpha=0.5)
    # configure the x axis 
    axs[0].xaxis.tick_top() 
    axs[0].set_xlim(0, 200)
    axs[0].set_xticks(arange(0, 201, 40))
    # create the secondary axis and scale it accordingly
    secax = axs[0].secondary_xaxis('bottom', functions=(lambda x: x * 2.5, lambda x: x / 2.5)) 
    secax.tick_params(axis='x', direction='in') # set the axis's tick marks location
    secax.set_xlabel('Rozegranych gier (×1000)')
    # set the border thicness
    for spine in axs[0].spines.values():
        spine.set_linewidth(1)

    #
    # changes to the second subplot
    #
    axs[1].yaxis.tick_right()
    axs[1].grid(which='both', color='darkgray', dashes=(1.2, 3.6))
    plt.setp(axs[1].get_xticklabels(), rotation=20, horizontalalignment='center')
    # set the border thicness
    for spine in axs[1].spines.values():
        spine.set_linewidth(0.7)

    fig.savefig('data_visualization/plot.pdf')
    plt.show()


def main() -> None:
    # read the data
    combined_data = []
    boxplot_combined_data = []
    for name in file_names:
        (data, boxplot_data) = (read_file(name))
        combined_data.append(data)
        boxplot_combined_data.append(boxplot_data)
    
    draw_plot(combined_data, boxplot_combined_data)


if __name__ == '__main__':
    main()