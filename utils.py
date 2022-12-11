async def formatDescription(text, hasImage=False):
    """
        Formats user input for image description,
        Returns a dictionary {"description": text, "n": number, "size": text}
    """
    response = {}
    splitted_text = text.split("%")
    if not hasImage:
        response.update({"description" : splitted_text[0].strip()})
        response.update({"n" : int(splitted_text[1].strip())})
        response.update({"size" : splitted_text[2].strip().lower()})
    else:
        response.update({"n" : int(splitted_text[0].strip())})
        response.update({"size" : splitted_text[1].strip().lower()})

    return response