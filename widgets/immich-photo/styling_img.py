import requests
import random
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

FONT = "YOUR_FONT.ttf"
EXPORT_PATH = "/path/to/glance/assets/memory.png"

BASE_URL = "https://IMMICH_URL:PORT"
API_KEY = "IMMICH_API_KEY"
PAYLOAD = {
    "page": 1,
    "withExif": True,
    "isVisible": True,
    "type": "IMAGE"
    }
# PAYLOAD = {
#     "page":1,
#     "withExif":True,
#     "isVisible":True,
#     "make":"samsung"
#     }

def get_assets():
    endpoint = f"{BASE_URL}/api/search/metadata"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    response = requests.post(endpoint, headers=headers, json=PAYLOAD)
    response.raise_for_status()
    return response.json()['assets']['items']

def filter_by_aspect_ratio(items, min_ratio=0.4, max_ratio=1.5):
    filtered = []
    for item in items:
        if not item.get('exifInfo'):
            continue
        width = item['exifInfo'].get('exifImageWidth', 0)
        height = item['exifInfo'].get('exifImageHeight', 0)
        if width == 0 or height == 0:
            continue
        ratio = width / height
        if min_ratio <= ratio <= max_ratio:
            filtered.append(item)
    return filtered

def get_random_asset(items):
    return random.choice(items) if items else None

def get_thumbnail(asset_id):
    endpoint = f"{BASE_URL}/api/assets/{asset_id}/thumbnail?size=preview"
    headers = {
        'Accept': 'image/*',
        'x-api-key': API_KEY
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def create_info_dict(asset):
    exif = asset.get('exifInfo', {})
    return {
        'id': asset['id'],
        'localDateTime': asset['localDateTime'],
        'make': exif.get('make'),
        'model': exif.get('model'),
        'fNumber': exif.get('fNumber'),
        'focalLength': exif.get('focalLength'),
        'iso': exif.get('iso'),
        'exposureTime': exif.get('exposureTime'),
        'city': exif.get('city'),
        'width': exif.get('exifImageWidth'),
        'height': exif.get('exifImageHeight'),
        'fileSize': exif.get('fileSizeInByte'),
        'orientation': exif.get('orientation')
    }

def load_icon(icon_path, target_height):
    try:
        icon_img = Image.open(icon_path).convert("RGBA")
        ratio = target_height / icon_img.height
        new_width = int(icon_img.width * ratio)
        return icon_img.resize((new_width, target_height), Image.LANCZOS)
    except:
        return None

def create_rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    
    draw.rectangle([(radius, 0), (size[0]-radius, size[1])], fill=255)
    draw.rectangle([(0, radius), (size[0], size[1]-radius)], fill=255)
    
    draw.ellipse([(0, 0), (radius*2, radius*2)], fill=255)
    draw.ellipse([(size[0]-radius*2, 0), (size[0], radius*2)], fill=255)
    draw.ellipse([(0, size[1]-radius*2), (radius*2, size[1])], fill=255)
    draw.ellipse([(size[0]-radius*2, size[1]-radius*2), (size[0], size[1])], fill=255)
    
    return mask

def add_frame_with_info(img, info_dict):
    width, height = img.size
    new_width = 700
    ratio = new_width / float(width)
    new_height = int(height * ratio)
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    top, left, right, bottom = 30, 30, 30, 120
    new_width_with_frame = new_width + left + right
    new_height_with_frame = new_height + top + bottom
    
    frame = Image.new('RGB', (new_width_with_frame, new_height_with_frame), (233, 219, 193))
    mask = create_rounded_mask((new_width_with_frame, new_height_with_frame), 16)
    frame.putalpha(mask)
    frame.paste(resized_img, (left, top))
    draw = ImageDraw.Draw(frame)
    
    try:
        font_model = ImageFont.truetype(FONT, 20)
        font_exif = ImageFont.truetype(FONT, 16)
        font_city_time = ImageFont.truetype(FONT, 24)
    except:
        default_font = ImageFont.load_default()
        font_model = default_font.font_variant(size=20)
        font_exif = default_font.font_variant(size=16)
        font_city_time = default_font.font_variant(size=24)
    
    # line1 in right: city and date
    line1_parts = []
    if 'city' in info_dict and info_dict['city']:
        line1_parts.append(info_dict['city'])    
    if 'localDateTime' in info_dict and info_dict['localDateTime']:
        try:
            dt = datetime.strptime(info_dict['localDateTime'], "%Y-%m-%dT%H:%M:%S.%f%z")
            line1_parts.append(dt.strftime("%Y %b").upper())
        except:
            pass
    if line1_parts:
        line1 = " | ".join(line1_parts)
        text_width = draw.textlength(line1, font=font_city_time)
        draw.text(((new_width_with_frame - text_width - right), new_height_with_frame - 72),
                 line1,
                 font=font_city_time,
                 fill=(0, 0, 0))
    
    text_y = new_height_with_frame - 90
    line_spacing = 40
    # line2 in left: make and model
    line2_parts = []
    icon_img = None
    if 'icon' in info_dict and info_dict['icon']:
        icon_img = load_icon(info_dict['icon'], 24)
    if 'model' in info_dict and info_dict['model']:
        line2_parts.append(info_dict['model'])
    if line2_parts or icon_img:
        elements = []
        if icon_img:
            elements.append(('image', icon_img))
        if line2_parts:
            line2_text = "·".join(line2_parts)
            elements.append(('text', line2_text))
        current_x = left
        for element in elements:
            if element[0] == 'image':
                frame.paste(element[1], (int(current_x), text_y), element[1])
                current_x += element[1].width + 10
            elif element[0] == 'text':
                draw.text((current_x, text_y),
                         "| ",
                         font=font_model,
                         fill=(100, 100, 100))
                draw.text((current_x + 20, text_y),
                         element[1],
                         font=font_model,
                         fill=(0, 0, 0))
                current_x += draw.textlength(element[1], font=font_model)
        
        text_y += line_spacing
    
    # line3 in left: focalLength, fNumber, exposureTime, iso
    line3_parts = []
    if 'focalLength' in info_dict and info_dict['focalLength']:
        line3_parts.append(f"{info_dict['focalLength']}mm")
    if 'fNumber' in info_dict and info_dict['fNumber']:
        line3_parts.append(f"f/{info_dict['fNumber']}")
    if 'exposureTime' in info_dict and info_dict['exposureTime']:
        line3_parts.append(f"{info_dict['exposureTime']}s")
    if 'iso' in info_dict and info_dict['iso']:
        line3_parts.append(f"ISO{info_dict['iso']}")
    if line3_parts:
        line3 = "  ".join(line3_parts)
        text_width = draw.textlength(line3, font=font_exif)
        draw.text((left, text_y),
                 line3,
                 font=font_exif,
                 fill=(100, 100, 100))
    return frame

if __name__ == "__main__":
    # info_dict = {
    #     "icon": "icons/sony.png",
    #     "make": "SONY",
    #     "model": "ILCE-6300",
    #     "localDateTime": "2024-02-01T00:00:00.000+00:00",
    #     "fNumber": 5.6,
    #     "focalLength": 135,
    #     "iso": 320,
    #     "exposureTime": "1/1600",
    #     "city": "泉州市 惠安县",
    # }
    # input_img = Image.open("input.jpg")

    all_assets = get_assets()
    filtered_assets = filter_by_aspect_ratio(all_assets, min_ratio=0.5, max_ratio=2.0)
    if not filtered_assets:
        print("No assets found with the specified aspect ratio.")
        exit(1)    
    selected_asset = get_random_asset(filtered_assets)
    info_dict = create_info_dict(selected_asset)

    # refine the info_dict
    if info_dict['make']:
        info_dict['icon'] = 'icons/' + info_dict['make'].lower() + ".png"
    # for Chinese user who set ZingLix/immich-geodata-cn package
    # if info_dict['city']:
    #     import re
    #     parts = re.findall(r'([^省市区县旗]+)(?:省|市|区|县|自治县|旗|自治旗)?', info_dict['city'])
    #     info_dict['city'] = ' · '.join(p.strip() for p in parts[:2])
    
    input_img = get_thumbnail(selected_asset['id'])

    if input_img is not None:
        output_img = add_frame_with_info(input_img, info_dict)
        output_img.save(EXPORT_PATH)
    else:
        print("Could not load image")