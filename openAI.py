import os
from io import BytesIO
from PIL import Image
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generateImageUrls(request, number_of_images, image_size):
    response = openai.Image.create(
        prompt = request,
        n = number_of_images,
        size = image_size
    )
    image_urls = response['data']
    return image_urls

async def resizeImage(image_):
    """Read the image file from disk and resize it"""
    image = Image.open(image_)
    size = max(image.size)
    if size <= 384:
        width, height = 256, 256
    elif size > 384 and size <= 768:
        width, height = 512, 512
    elif size > 768:
        width, height = 1024, 1024
    image = image.resize((width, height))
    return image

async def convertImageToByte(image):
    """Convert the image to a BytesIO object"""
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    return byte_array

async def generateVariationUrls(request, number_of_images, image_size):
    image = await resizeImage(request)
    byte_array = await convertImageToByte(image)
    response = openai.Image.create_variation(
        image = byte_array,
        n = number_of_images,
        size = image_size
    )
    image_urls = response['data']
    return image_urls