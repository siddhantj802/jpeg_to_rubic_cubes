from PIL import Image
import os 

size = (128, 128)
input_path = "./input_images/sellerimg.png"
output_dir = "./saved_images"
output_path = os.path.join(output_dir , "sellerimg_resized.png")
try:
     with Image.open(input_path) as img:
        print(f"Original Image size is {img.size}")
        img.thumbnail(size)
        print(f"New Image size is {img.size}")
        img.save(output_path)
        print("Image saved successfully")
except FileNotFoundError:
    print("Image not Found")
except Exception as e:
    print("something went wrong",e)
finally:
    print("Operation Complete")
