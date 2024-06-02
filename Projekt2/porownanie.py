from PIL import Image
import numpy as np

def calculate_brightness(pixel):
    # Jasność jako średnia wartości RGB
    return int((pixel[0] + pixel[1] + pixel[2]) / 3)

def image_difference(image1_path, image2_path, output_path):
    # Wczytanie obrazów
    image1 = Image.open(image1_path).convert("RGB")
    image2 = Image.open(image2_path).convert("RGB")

    # Upewnienie się, że obrazy mają ten sam rozmiar
    if image1.size != image2.size:
        raise ValueError("Obrazy muszą mieć ten sam rozmiar")

    # Konwersja obrazów do tablic numpy
    pixels1 = np.array(image1)
    pixels2 = np.array(image2)

    # Obliczenie różnicy jasności
    difference = np.abs(pixels1.astype(int) - pixels2.astype(int))

    # Przekształcenie różnicy do formatu obrazu
    difference_image = Image.fromarray(np.uint8(difference))

    # Zapisanie wyniku
    difference_image.save(output_path)

# Ścieżki do obrazów wejściowych
image1_path = 'ecb_decrypted_image.png'
image2_path = 'ecb_decompressed_decrypted_image.png'

# Ścieżka do obrazu wyjściowego
output_path = 'difference_image.png'


# Obliczenie różnicy i zapisanie obrazu
image_difference(image1_path, image2_path, output_path)




