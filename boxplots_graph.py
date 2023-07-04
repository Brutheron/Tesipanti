import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar
import pickle

# open the pickle file
with open('hue_values_dict_sorted.pickle', 'rb') as f:
    hue_values_dict = pickle.load(f)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(20, 10))  # adjust the size to fit more boxplots

# create a DataFrame from the hue_values_dict
df = pd.DataFrame.from_dict({(i,j): hue_values_dict[i][j] 
                           for i in hue_values_dict.keys() 
                           for j in hue_values_dict[i].keys()},
                           orient='index')

# for the first folder only keep the '1.png' and for the rest keep '2.png'
df = df.loc[[(list(hue_values_dict.keys())[0],'1.png')] + [(i, '2.png') for i in list(hue_values_dict.keys())[1:]]]
df = df.dropna(axis=1)
df = df.transpose()

# Plot the boxplot on the axes
sns.set(style="whitegrid")
box_plot = sns.boxplot(ax=ax, data=[df.iloc[:,x].values for x in range(11)], palette="Set3", orient='h')

# You can set your own labels here
box_plot.set(
    xlabel="Hue",
    ylabel="Dosis de MB",  # Modify as needed
    title=f"Comparación antes y después de cada indicador MB",
)
yticks = ["Antes"] + [f"MB: {df.columns[x][0]/10}" for x in range(len(df.columns[1:]))]
plt.yticks(range(len(yticks)), yticks)  # set the y-ticks to the image names

# Set the color of all boxes except the first one
for i, box in enumerate(box_plot.artists):
    if i != 0:  # change the index as per your requirement
        box.set_facecolor('skyblue')

# Create colorbar
cmap = mpl.cm.hsv  # Use a standard HSV colormap
norm = mpl.colors.Normalize(vmin=0, vmax=360)  # Range of your hue values
cax = fig.add_axes([0.93, 0.1, 0.02, 0.8])  # Adjust the size and position of the colorbar
cb = mcolorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

plt.savefig("boxplots.png")
