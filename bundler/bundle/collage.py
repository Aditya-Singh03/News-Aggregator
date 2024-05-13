from typing import List
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import unquote
import PIL
import pyimgur
from bundle.utils import IMGUR_CLIENT_ID
import os
from uuid import uuid4


def make_collage(source_media: List[str]) -> str:
    if len(source_media) < 2:
        return source_media[0]

    links = list(
        map(unquote, filter(lambda link: link.startswith("http"), source_media))
    )
    response_content: List[str] = []

    for link in links:
        try:
            response_content.append(requests.get(link, timeout=5).content)
        except requests.exceptions.RequestException as e:
            print("Failed to retrieve image", e)

    if len(response_content) >= 4:
        response_content = response_content[:4]
    elif len(response_content) >= 2:
        response_content = response_content[:2]
    else:
        return source_media[0]

    photos = []
    for content in response_content:
        try:
            photo = Image.open(BytesIO(content)).convert("RGBA")
            photos.append(photo)
        except Exception as e:
            print("Failed to open image", e)

    if len(photos) < 2:
        return source_media[0]

    myWidth = 500
    hsizeArr = [
        int((float(img.size[1]) * float((myWidth / float(img.size[0])))))
        for img in photos
    ]

    common_height = min(hsizeArr)
    photos = [
        photo.resize((myWidth, common_height), PIL.Image.LANCZOS) for photo in photos
    ]

    total_width = myWidth * 2
    total_height = common_height * (len(photos) // 2 + len(photos) % 2)
    collage = Image.new(
        "RGBA", (int(total_width), int(total_height)), (255, 255, 255, 0)
    )
    xOffset = yOffset = 0

    for photo, hsize in zip(photos, hsizeArr):
        collage.paste(photo, (xOffset, yOffset))
        xOffset += myWidth
        if xOffset >= total_width:
            xOffset = 0
            yOffset += hsize

    college_filepath = os.path.join("images", f"{uuid4()}.png")
    collage.save(college_filepath)

    imgur_link = upload_to_imgur(college_filepath)
    os.remove(college_filepath)
    return imgur_link


def upload_to_imgur(image_path: str) -> str:
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(image_path, title="News Aggregator Collage")
    return uploaded_image.link
