from PIL import Image

def read_png_file(file_path):
    # Otwórz plik PNG
    image = Image.open(file_path)
    # Przekonwertuj obraz na dane pikseli (opcjonalnie, jeśli chcesz uzyskać dostęp do pikseli)
    pixels = list(image.getdata())
    # Wyświetl podstawowe informacje o obrazie
    print(f"Format: {image.format}")
    print(f"Rozmiar: {image.size}")
    print(f"Tryb: {image.mode}")
    return image

file_path = 'image.png'
image = read_png_file(file_path)

# Opcjonalnie możesz uzyskać dostęp do danych pikseli
pixels = list(image.getdata())
print(pixels)
