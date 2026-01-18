from PIL import Image,ImageDraw
from collections import Counter
import itertools
import json
import os
input_path = "./input_images/sellerimg.png"
output_dir = './saved_images'
output_path = os.path.join(output_dir, "sellerimg_resize.png")

# hard coded size; maybe change in future
#size = (20 , 20)
cube_size = 200
gap = 10
border_thickness = 20
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

try:
    os.makedirs(output_dir, exist_ok=True)

    with Image.open(input_path) as img:
        #Never use [[...]] * n for 2D arrays unless you want shared references (almost never).
        color_grid = [[0]*img.size[1] for _ in range(img.size[0])]
        grid_width = len(color_grid) # 406
        grid_height = len(color_grid[0]) # 333  # 406 x 333
        print(f"grid_width is {grid_width} grid_height is {grid_height}")
        img_width = grid_width * (cube_size+gap)
        img_height = grid_height * (cube_size+gap)

        #resized_img = img.resize(size)
        rgb_img = img.convert('RGB')
        width,height = rgb_img.size
        print(f"width is {width} height is {height}")
        for x in range(width):
            for y in range(height):
                shortest_distance = float('inf')
                shortest_color = ''
                #print(f"rgb for {x},{y} pixel is {rgb_img.getpixel((x,y))}")
                r_value, g_value , b_value = rgb_img.getpixel((x,y))
                for color_key , (cr,cg,cb) in cube_color.items():
                    distance = abs(cr-r_value)+abs(cb-b_value)+abs(cg-g_value)
                    if shortest_distance > distance:
                        shortest_distance = distance
                        shortest_color = color_key

                color_grid[x][y] = shortest_color
        #print(color_grid)            
        color_counter = dict(Counter(itertools.chain(*color_grid))) # "*" is an unpacking operator; it unpacks 2D array for the Counter function.
        
    with open('./output/cube_layout.json', 'w') as f:
        json.dump(color_grid , f)
                
    output_img = Image.new(mode="RGB", size=(img_width,img_height),  color = (211, 211, 211))    
    draw = ImageDraw.Draw(output_img)
    for x in range(grid_height):
        for y in range(grid_width):
            pixel_x = x * 21 
            pixel_y = y * 21
            right  = pixel_x + cube_size
            bottom = pixel_y + cube_size
            
            cube_name = color_grid[x][y]
            rgb_color = cube_color[cube_name]
            
            
            draw.rectangle(xy=(pixel_x,pixel_y,right,bottom), fill=rgb_color,outline=(153,153,134),width=border_thickness)
    output_img.save((os.path.join(output_dir , "mosaic_img.png")))
    output_img.show()
            
            
except FileNotFoundError:
    print("File Not Found")
except Exception as e:
    print("something went wrong",e)
finally:

    print('Operation Complete')


