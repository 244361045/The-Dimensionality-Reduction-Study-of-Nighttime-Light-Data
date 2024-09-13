import os
from PIL import Image
import numpy as np


def preprocess_image(image, size=16):
    return image.resize((size, size), Image.LANCZOS).convert('L')


def average_hash(image):
    image = preprocess_image(image)
    pixels = np.array(image, dtype=np.uint8)
    avg = pixels.mean()
    return ''.join('1' if x < avg else '0' for x in pixels.flatten())


def visualize_hash(hash_str, size=16, square_size=20, border_width=1):
    total_size = size * (square_size + border_width) - border_width + 2
    image = Image.new('1', (total_size, total_size), "black")
    pixels = image.load()

    for i, bit in enumerate(hash_str):
        col = i % size * (square_size + border_width) + 1
        row = i // size * (square_size + border_width) + 1
        for y in range(square_size):
            for x in range(square_size):
                pixels[col + x, row + y] = 255 if bit == '1' else 0

    return image


def process_images(source_folder, target_folder):
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(source_folder, filename)
            image = Image.open(image_path)
            hash_code = average_hash(image)
            visualized_hash = visualize_hash(hash_code)

            output_path = os.path.join(target_folder, f'{filename}')
            visualized_hash.save(output_path)
            print(f"Processed and saved: {output_path}")



source_folder = ''
target_folder = ''


process_images(source_folder, target_folder)