import requests
from PIL import Image
from io import BytesIO
from urllib.parse import unquote


image_links= [
    unquote('https://cdn.theathletic.com/app/uploads/2024/04/27151625/USATSI_23127346-scaled.jpg'),
    unquote('https://media.wired.com/photos/6603759fd3a75d0aa76d16ab/191:100/w_1280,c_limit/business_crypto_tracing_forensics_trial.jpg'),
    unquote('https://readwrite.com/wp-content/uploads/2024/04/zxDgyfq8QYCzJhRAH2CF1g.jpg'),
    unquote('https://assets3.cbsnewsstatic.com/hub/i/r/2023/02/23/3690b4ba-277c-4748-8e69-f8177a4dd703/thumbnail/1200x630/26f6f42c56a88f7c4346b3d641864a9b/hypatia-h-2ceb6723b01f0f70c71123555aebe0b4-h-09ed3669efb44602e3b3c5d177a449b8.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4"')
]


collage = Image.new("RGBA", (500,500), color=(255,255,255,255))
responses = [requests.get(image_link) for image_link in image_links]
photos = [Image.open(BytesIO(response.content)).convert("RGBA") for response in responses]
photos = [photo.resize((250,250)) for photo in photos]
index=0;
for i in range(0,500,250):
    for j in range(0,500,250):
        if(index < len(photos)):
            collage.paste(photos[index], (i,j))
            index+=1
        else:
            break
    

collage.show()
