import asyncio
import requests
import base64
import urllib.parse
import shlex

async def get_image(message, user_key):
    my_prompt, my_nprompt, res, do_base, do_nbase = parse_message(message.content)

    user_feedback = "Generating image"

    if my_prompt != "":
        user_feedback += ", prompt: '" + my_prompt + "'"
    if my_nprompt != "":
        user_feedback += ", negative prompt: '" + my_nprompt + "'"
    if res != "":
        user_feedback += ", resolution: '" + res + "'"
    if not do_base:
        user_feedback += ", no base prompt"
    if not do_nbase:
        user_feedback += ", no negative base prompt"

    await message.channel.send(user_feedback)

    if do_base:
        base_prompt = ", concept art, digital art, illustration, league of legends style concept art, inspired by wlop style, 8k, fine details, sharp, very detailed, high resolution"
    else:
        base_prompt = ""
    prompt = urllib.parse.quote(my_prompt + base_prompt)

    if do_nbase:
        base_nprompt = ", low-quality, deformed, text, poorly drawn"
    else:
        base_nprompt = ""
    nprompt = urllib.parse.quote(my_nprompt + base_nprompt)

    baseurl = ["https://image-generation.perchance.org/textToImage?prompt=",
               "&seed=-1&resolution=",
               "&guidanceScale=7&negativePrompt=",
               "&channel=ai-text-to-image-generator&userKey=" + user_key]

    if res == "portrait":
        res = "512x768"
    elif res == "landscape":
        res = "768x512"
    elif res == "square":
        res = "512x512"

    url = baseurl[0] + prompt + baseurl[1] + res + baseurl[2] + nprompt + baseurl[3]

    # await message.channel.send("Requesting image from " + url)
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url)
    r = await asyncio.wrap_future(future)

    if r.status_code != 200 or r.json()["status"] != "success":
        await message.channel.send("Error: code: " + str(r.status_code) + ", status: " + r.json()["status"])
        return

    img_data = r.json()["imageDataUrls"]
    img_data = img_data[0].split(",")[1]
    img = base64.b64decode(img_data)
    img_name = "latest_stablediff_img.png"
    with open(img_name, 'wb') as f:
        f.write(img)
    return img_name

def parse_message(message):
    message = shlex.split(message)
    prompt = ""
    nprompt = ""
    res = "portrait"
    do_base = True
    do_nbase = True
    for i in range(len(message)):
        if message[i] == "-p":
            prompt = message[i + 1]
        elif message[i] == "-np":
            nprompt = message[i + 1]
        elif message[i] == "-r":
            res = message[i + 1]
        elif message[i] == "-nb":
            do_base = False
        elif message[i] == "-nnb":
            do_nbase = False
    return prompt, nprompt, res, do_base, do_nbase