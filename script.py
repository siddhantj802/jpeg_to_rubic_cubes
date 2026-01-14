from PIL import Image
import os
input_path = "./input_images/sellerimg.png"
output_dir = './saved_images'
output_path = os.path.join(output_dir, "sellerimg_resize.png")

# hard coded size; maybe change in future
size = (20 , 20)

#hard coded cube color values
cube_color = {
    'White'   : (255, 255, 255),
    'Yellow'  : (255, 255,   0),
    'Red'     : (255,   0,   0),
    'Orange'  : (255, 165,   0),
    'Blue'    : (  0,   0, 255),
    'Green'   : (  0, 255,   0)
}
#Never use [[...]] * n for 2D arrays unless you want shared references (almost never).
color_grid = [[0]*size[0] for _ in range(size[1])]
try:
    os.makedirs(output_dir, exist_ok=True)

    with Image.open(input_path) as img:
        resized_img = img.resize(size)
        rgb_img = resized_img.convert('RGB')
        width,height = rgb_img.size
        for y in range(height):
            for x in range(width):
                shortest_distance = float('inf')
                shortest_color = ''
                #print(f"rgb for {x},{y} pixel is {rgb_img.getpixel((x,y))}")
                r_value, g_value , b_value = rgb_img.getpixel((x,y))
                for color_key , (cr,cg,cb) in cube_color.items():
                    distance = abs(cr-r_value)+abs(cb-b_value)+abs(cg-g_value)
                    if shortest_distance > distance:
                        shortest_distance = distance
                        shortest_color = color_key

                color_grid[y][x] = shortest_color
                    
        print(color_grid)        
        
except FileNotFoundError:
    print("File Not FOund")
except Exception as e:
    print("something went wrong",e)
finally:

    print('Operation Complete')

