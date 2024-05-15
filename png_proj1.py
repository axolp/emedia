from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def spectrum(file_name):
    # Open the image and convert to grayscale
    img = Image.open(file_name)
    img_gray = img.convert('L')
    
    # Convert image data to a numpy array
    data = np.array(img_gray)
    
    # Use only the first 1000 samples if the image is large enough
    data_samples = data
    
    # Perform a 2D Fast Fourier Transform
    fft_result = np.fft.fft2(data_samples)
    fft_shift = np.fft.fftshift(fft_result)
    
    # Compute magnitude and phase spectrums
    magnitude_spectrum = np.log(np.abs(fft_shift))
    phase_spectrum = np.angle(fft_shift)
    
    # Create a new figure for this specific image analysis
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Display the original image samples
    axes[0].imshow(data_samples, cmap='gray')
    axes[0].set_title('Original Image (first 1000 samples)')
    axes[0].axis('off')

    # Display the magnitude spectrum
    axes[1].imshow(magnitude_spectrum, cmap='jet', extent=[-0.5, 0.5, -0.5, 0.5])
    axes[1].set_title('Magnitude Spectrum')
    axes[1].axis('on')

    # Display the phase spectrum
    axes[2].imshow(phase_spectrum, cmap='gray')
    axes[2].set_title('Phase Spectrum')
    axes[2].axis('off')

    # Set a title for the whole figure
    fig.suptitle(file_name, fontsize=16)

    # Adjust layout and show the plot in a new window
    plt.tight_layout()
    plt.show()



def readMetaData(file_name):
    with open(file_name, 'rb') as file:
        return file.read()

def writeMetaData(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)  

def readHeader(path):
    with open(path, 'rb') as file:
        file_bytes = file.read()
        file_length = len(file_bytes)
        hex_representation = file_bytes.hex()

    png_signature = hex_representation[:16]
    ihdr = hex_representation[16:42+8]

    ihdr_length = int(ihdr[:8], 16)
    ihdr_ascii = int(ihdr[8:8+8], 16)
    image_width = int(ihdr[16:16+8], 16)
    image_height = int(ihdr[24:24+8], 16)
    image_depth = int(ihdr[32:32+2], 16)

    print(f'Length of the file: {file_length} bytes')
    print(f'PNG Signature: {png_signature}')  
    print(f'IHDR: {ihdr}')
    print(f'IHDR length: {ihdr_length}')
    #print(f'IHDR adcii: {ihdr_ascii}')
    print(f'image width: {image_width}')
    print(f'image height: {image_height}')
    print(f'image depth: {image_depth}')
    return 

def make_message(n):
    global idx
    m= ""
    for i in range(n):
        if i+idx == len(secret_message) - 1:
            m+="0"
        else:
            m+=secret_message[i+idx]
            idx+=1
    return m
def first_point():
    readHeader("black1.png")

#def second_point():
    #WKLEJ SWOJE

def third_point():
    ancillary_chunks = [
        "6348524D",  # cHRM
        "67414D41",  # gAMA
        "73424954",  # sBIT
        "624B4744",  # bKGD
        "68495354",  # hIST
        "74524E53",  # tRNS
        "70485973",  # pHYs
        "74494D45",  # tIME
        "74455874",  # tEXt
        "7A545874"   # zTXt
    ]

    pwr_hex= "50575220"
    binary_file = readMetaData("black1.png")

    hex_data = binary_file.hex()
    new_hex_data= hex_data
    test_data=hex_data


    for chunk_code in ancillary_chunks:
        if chunk_code.lower() in new_hex_data:
            index= new_hex_data.find(chunk_code.lower())
            print(f"Found ancillary chunk: {chunk_code}, index: {index}")
            #print("mine", hex_data[index:index+8])
        
            ancillary_length_h= new_hex_data[index-8:index]
            ancillary_length= int(ancillary_length_h, 16)
            new_m=  make_message(ancillary_length)
            ancillary_data= new_hex_data[index+8:index+8+ancillary_length]
            crc= new_hex_data[index+8+ancillary_length:index+8+ancillary_length+8]
            print("data", ancillary_length, new_m,  ancillary_data, crc)
            new_hex_data = new_hex_data[:index+8] + make_message(ancillary_length) + new_hex_data[index+8+ancillary_length:]
            new_hex_data = new_hex_data[:index+8+ancillary_length] + pwr_hex + new_hex_data[index+8+ancillary_length+8:]
            print(ancillary_length)


    if '49444154' in hex_data:
        print("Found IDAT")
    new_binary_data = bytes.fromhex(new_hex_data)
    test_data = bytes.fromhex(test_data)
    writeMetaData("modified.png", new_binary_data)

# idx= 0
# # Meet me on the PWR C3 after dark. 51.108811,17.060266 in hex
# secret_message= "4d656574206d65206f6e2074686520505752204333206166746572206461726b2e2035312e3130383831312c31372e303630323636" 



# first_point()
# #second_point()
# third_point()

spectrum('black_grad.png')
# spectrum('test_spectre_cut.png')
# spectrum('test_spectre_centre.png')