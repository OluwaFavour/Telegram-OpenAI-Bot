import os
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