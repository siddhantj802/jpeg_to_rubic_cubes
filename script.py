from PIL import Image, ImageDraw
from collections import Counter
import itertools
import os

input_path = "./input_images/sellerimg.png"
output_dir = './saved_images'

# Adjust these values
CUBE_SIZE = 50
GAP = 2
BORDER_THICKNESS = 1
MAX_INPUT_DIMENSION = 200  # Maximum dimension for input image
MAX_OUTPUT_DIMENSION = 4000  # Maximum dimension for output image

cube_color = {
    'White': (255, 255, 255),
    'Yellow': (255, 255, 0),
    'Red': (255, 0, 0),
    'Orange': (255, 165, 0),
    'Blue': (0, 0, 255),
    'Green': (0, 255, 0)
}

try:
    os.makedirs(output_dir, exist_ok=True)
    
    with Image.open(input_path) as img:
        print(f"Original image: {img.size}")
        
        # Resize input if too large
        if max(img.size) > MAX_INPUT_DIMENSION:
            ratio = MAX_INPUT_DIMENSION / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"Resized to: {img.size}")
        
        width, height = img.size
        
        # Calculate optimal cube size based on desired output
        desired_cube_size = CUBE_SIZE
        estimated_width = width * (desired_cube_size + GAP)
        estimated_height = height * (desired_cube_size + GAP)
        
        # If output would be too large, reduce cube size
        if max(estimated_width, estimated_height) > MAX_OUTPUT_DIMENSION:
            max_cube_from_output = MAX_OUTPUT_DIMENSION // max(width, height) - GAP
            cube_size = max(50, max_cube_from_output)  # Minimum 50px
            print(f"Reducing cube size from {desired_cube_size} to {cube_size}")
        else:
            cube_size = desired_cube_size
        
        print(f"Using cube size: {cube_size}")
        
        # Create color grid
        color_grid = [[0] * width for _ in range(height)]
        rgb_img = img.convert('RGB')
        
        for y in range(height):
            for x in range(width):
                r, g, b = rgb_img.getpixel((x, y))
                best_color = min(cube_color.items(),
                               key=lambda item: sum((c1 - c2) ** 2 for c1, c2 in zip(item[1], (r, g, b))))
                color_grid[y][x] = best_color[0]
        
        # Calculate output size
        img_width = width * (cube_size + GAP) + GAP
        img_height = height * (cube_size + GAP) + GAP
        
        print(f"Output will be: {img_width} x {img_height} pixels")
        print(f"Memory estimate: {(img_width * img_height * 3) / (1024**2):.1f} MB")
        
        # Check if output is too large
        if img_width * img_height > 10000 * 10000:  # 100MP limit
            print("Warning: Output would be very large!")
            print("Consider reducing cube size or input image size further")
        
        # Create output image
        output_img = Image.new("RGB", (img_width, img_height), (211, 211, 211))
        draw = ImageDraw.Draw(output_img)
        
        # Draw cubes
        for row in range(height):
            for col in range(width):
                left = col * (cube_size + GAP) + GAP
                top = row * (cube_size + GAP) + GAP
                right = left + cube_size
                bottom = top + cube_size
                
                cube_name = color_grid[row][col]
                rgb_color = cube_color[cube_name]
                
                draw.rectangle(
                    (left, top, right, bottom),
                    fill=rgb_color,
                    outline=(100, 100, 100),
                    width=BORDER_THICKNESS
                )
        
        # Save with optimization
        output_path = os.path.join(output_dir, "mosaic.jpg")
        output_img.save(output_path, "JPEG", quality=90, optimize=True)
        print(f"Saved to: {output_path} ({(os.path.getsize(output_path) / 1024):.1f} KB)")
        
        # Create a smaller preview for display
        preview_size = (min(1200, img_width), min(800, img_height))
        if img_width > preview_size[0] or img_height > preview_size[1]:
            preview = output_img.copy()
            preview.thumbnail(preview_size, Image.Resampling.LANCZOS)
            preview.show()
        else:
            output_img.show()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()