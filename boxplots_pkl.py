import os
import numpy as np
from PIL import Image
import colorsys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar
import pickle

topdir = "fotos tesis finales"  # Replace with the path to your directory
hue_values_dict = {} # dictionary to store the hue values

# loop over the folders
for folder in os.listdir(topdir):
    
    # create a dictionary for each folder
    experiment_number = int(folder[2:])
    hue_values_dict[experiment_number] = {}
    
    # show which folder is being processed
    print(folder)
    
    # loop over the images in the folder
    folder_path = os.path.join(topdir, folder)
    if os.path.isdir(folder_path):
        # List for storing hue values of both images
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
                hue_values_dict[experiment_number][image_name] = hue_values_no_outliers

with open('hue_values_dict_sorted.pickle', 'wb') as handle:
    hue_values_dict_sorted = dict(sorted(hue_values_dict.items()))
    pickle.dump(hue_values_dict_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)
