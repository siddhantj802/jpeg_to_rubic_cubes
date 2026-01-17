from PIL import Image,ImageDraw
from collections import Counter
import itertools
import json
import os
input_path = "./input_images/sellerimg.png"
output_dir = './saved_images'
output_path = os.path.join(output_dir, "sellerimg_resize.png")

# hard coded size; maybe change in future
size = (200 , 200)
cube_size = 20
gap = 2
border_thickness = 3
border_color = (0,0,0)

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
grid_height = len(color_grid)
grid_width = len(color_grid[0])

img_width = grid_width * (cube_size+gap)
img_height = grid_height * (cube_size+gap)
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
                    
        color_counter = dict(Counter(itertools.chain(*color_grid))) # "*" is an unpacking operator; it unpacks 2D array for the Counter function.
        
    with open('./output/cube_layout.json', 'w') as f:
        json.dump(color_grid , f)
                  
    output_img = Image.new(mode="RGB", size=(img_width,img_height),  color = (211, 211, 211))    
    
    
    x = 0
    y = 0
    pixel_x = 0 * 22 
    pixel_y = 0 * 22 
    draw = ImageDraw.Draw(output_img)
    draw.rectangle(xy=(pixel_x,pixel_y,img_height,img_width), fill=(0,0,0),outline=(153,153,134),width=border_thickness)
    output_img.save((os.path.join(output_dir , "mosaic_img.png")))
    output_img.show()
except FileNotFoundError:
    print("File Not Found")
except Exception as e:
    print("something went wrong",e)
finally:

    print('Operation Complete')


