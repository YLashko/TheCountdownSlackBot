from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def place_text_on_image(image_in_path: str, image_out_path: str, font_path: str, position: tuple[int], text: str):
    image_in = Image.open(image_in_path)
    font = ImageFont.truetype(font_path, 24)
    text_drawer = ImageDraw.Draw(image_in)
    text_drawer.text(position, text, font=font, fill=(0, 0, 0))
    image_in.save(image_out_path)
