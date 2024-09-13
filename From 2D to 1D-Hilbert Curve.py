import os
import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve
from PIL import Image
import numpy as np
import pandas as pd

input_folder_path = r''
output_folder_path = r''

all_images_data = []

grid_size = 16
order = 4
num_points = 2 ** (2 * order)


hilbert_curve = HilbertCurve(p=order, n=2)


for filename in os.listdir(input_folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg')):

        image_path = os.path.join(input_folder_path, filename)

        image = Image.open(image_path)
        image = image.resize((grid_size, grid_size), Image.LANCZOS)
        image = image.convert('1')
        image_array = np.array(image, dtype=np.uint8)
        image_array = np.flipud(image_array)

        hilbert_values = []

        fig, ax = plt.subplots(figsize=(8, 8))
        for i in range(grid_size + 1):
            ax.axhline(y=i, color='black', linestyle='-', linewidth=1)
            ax.axvline(x=i, color='black', linestyle='-', linewidth=1)
        plt.xticks([])
        plt.yticks([])
        ax.set_aspect('equal')
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)

        half_grid_step = 0.5
        x_coords_centered = [x + half_grid_step for x, _ in hilbert_curve.points_from_distances(range(num_points))]
        y_coords_centered = [grid_size - 1 - y + half_grid_step for _, y in
                             hilbert_curve.points_from_distances(range(num_points))]  # 翻转y坐标

        for (x, y) in zip(x_coords_centered, y_coords_centered):
            orig_x, orig_y = int(x - half_grid_step), int(y - half_grid_step)
            value = image_array[orig_y, orig_x]
            hilbert_values.append(value)
            color = 'white' if value == 1 else 'black'
            ax.add_patch(plt.Rectangle((x - half_grid_step, y - half_grid_step), 1, 1, color=color))

        ax.plot(x_coords_centered, y_coords_centered, 'b-', linewidth=1, zorder=2)

        processed_image_path = os.path.join(output_folder_path, f'{filename}')
        fig.savefig(processed_image_path, format='jpg', dpi=300)
        plt.close(fig)

        all_images_data.append([filename] + hilbert_values)

columns = ['Image Name'] + [f'Node {i + 1}' for i in range(num_points)]
df = pd.DataFrame(all_images_data, columns=columns)

excel_path = os.path.join(output_folder_path, 'hilbert_curve_binary_info.xlsx')
df.to_excel(excel_path, index=False)

print(f'Excel file has been saved to {excel_path}')
