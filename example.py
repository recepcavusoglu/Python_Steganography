import Steganography as stg

if __name__ == "__main__":
    stega_img = stg.Steganography("sample.jpg")
    stega_img.Write_Image("Hello There Image File!")
    print(stega_img.Read_Image("Steganography.bmp"))

    stega_audio=stg.Steganography("sample.wav")
    stega_audio.Write_Audio("Hello There Audio File!")
    print(stega_audio.Read_Audio("Steganography.wav"))
