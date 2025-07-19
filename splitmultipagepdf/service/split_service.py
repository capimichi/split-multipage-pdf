from injector import inject
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from tqdm import tqdm


class SplitService:

    @inject
    def __init__(self):
        pass

    def split(self, input_path: str, output_path: str, dpi: int = 200):
        # Convert PDF pages to images
        images = convert_from_path(input_path, dpi=dpi)

        output_images = []

        image_index = 0
        for image in tqdm(images, desc="Splitting PDF pages", unit="page"):
            bw_image = image.convert('1')
            
            # Convert each pixel to black and white if average RGB value is above a threshold
            rgb_threshold = 128
            bw_image = bw_image.point(lambda p: 255 if p > rgb_threshold else 0)

            # Process columns: if a column contains black pixels, make entire column black
            pixels = bw_image.load()
            width, height = bw_image.size
            
            for x in range(width):
                has_black_pixel = False
                # Check if column has any black pixels
                for y in range(height):
                    if pixels[x, y] == 0:  # Black pixel found
                        has_black_pixel = True
                        break
                
                # If column has black pixels, make entire column black
                if has_black_pixel:
                    for y in range(height):
                        pixels[x, y] = 0

            middle_column = width // 2

            checking_columns = range(middle_column - 100, middle_column + 100)
            # reverse checking_columns
            checking_columns = list(reversed(checking_columns))
            
            checking_columns = list(set(checking_columns))  # Remove duplicates
            
            found_x = None
            for x in checking_columns:
                has_black_pixel = False
                if pixels[x, 0] == 0:  # Black pixel found
                    has_black_pixel = True
                if not has_black_pixel:
                    found_x = x
                    break
            
            # split the image at found_x
            if found_x is not None:
                left_image = image.crop((0, 0, found_x, height))
                right_image = image.crop((found_x, 0, width, height))
                
                # left_image.save(f"tmp/page_{image_index}_left.png", "PNG")
                # right_image.save(f"tmp/page_{image_index}_right.png", "PNG")
                
                output_images.append(left_image)
                output_images.append(right_image)
            

            image_index += 1
        
        # Create a PDF from the output images
        if output_images:
            output_images[0].save(output_path, save_all=True, append_images=output_images[1:], resolution=dpi)




