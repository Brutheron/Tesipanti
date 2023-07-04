import os
import numpy as np
from PIL import Image
import colorsys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar

topdir = "fotos tesis finales"  # Replace with the path to your directory

for folder in os.listdir(topdir):
    print(folder)
    folder_path = os.path.join(topdir, folder)
    if os.path.isdir(folder_path):
        # List for storing hue values of both images
        hue_values_list = []
        for image_name in ["1.png", "2.png"]:
            image_path = os.path.join(folder_path, image_name)

            if os.path.isfile(image_path):
                image = Image.open(image_path)

                # Convert the image to RGBA mode
                image = image.convert("RGBA")

                # Convert the image to a NumPy array
                image_array = np.array(image)

                # Remove completely transparent pixels
                non_transparent_pixels = image_array[image_array[..., -1] != 0]

                # Normalize RGB values and convert to HSV
                hsv_pixels = np.array(
                    [
                        colorsys.rgb_to_hsv(
                            pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0
                        )
                        for pixel in non_transparent_pixels
                    ]
                )

                # Take the hue values (first column)
                hue_values = hsv_pixels[:, 0] * 360
                
                # exclude outliers using the IQR
                # Calculate IQR
                Q1 = np.percentile(hue_values, 25)
                Q3 = np.percentile(hue_values, 75)
                IQR = Q3 - Q1

                # Define a mask for values within 1.5*IQR of Q1 and Q3
                mask = ((Q1 - 1.5 * IQR <= hue_values) & (hue_values <= Q3 + 1.5 * IQR))

                # Apply mask to get hue values without outliers
                hue_values_no_outliers = hue_values[mask]
                
                # append the hue values to the list
                hue_values_list.append(hue_values_no_outliers)

                
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the boxplot on the axes
    sns.set(style="whitegrid")
    box_plot = sns.boxplot(ax=ax, data=hue_values_list, palette="Set3")

    # plot title MB measurement comes from folder name
    measurement = int(folder[2:])

    # You can set your own labels here
    box_plot.set(
        xlabel="Image",  # Modify as needed
        ylabel="Hue",
        title=f"Comparación antes y después del indicador MB: {measurement/10}",
    )
    plt.xticks([0, 1], ["1.png", "2.png"])  # Modify as needed

    # Create colorbar
    cmap = mpl.cm.hsv  # Use a standard HSV colormap
    norm = mpl.colors.Normalize(vmin=0, vmax=360)  # Range of your hue values
    cax = fig.add_axes([0.93, 0.1, 0.02, 0.8])  # Adjust the size and position of the colorbar
    cb = mcolorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

    plt.savefig(os.path.join(folder_path, "boxplot.png"))
