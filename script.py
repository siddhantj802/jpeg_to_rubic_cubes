from PIL import Image
import os
input_path = "./input_images/sellerimg.png"
output_dir = './saved_images'
output_path = os.path.join(output_dir, "sellerimg_resize.png")
size = (20 , 20)

try:
    with Image.open(input_path) as img:
        resized_img = img.resize(size)
        rgb_img = resized_img.convert('RGB')
        for x in range(20):
            for y in range(20):
                print(f"rgb for {x},{y} pixel is {rgb_img.getpixel((x,y))}")
except FileNotFoundError:
    print("File Not FOund")
except Exception as e:
    print("something went wrong",e)
finally:
    rgb_img.save(output_path)
    rgb_img.show()
    print('Operation Complete')

