#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import requests
import random
from langchain_community.llms import Ollama
from langchain import PromptTemplate
import os
import pyautogui as auto
import time

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images


def upload_file(file, subfolder="", overwrite=False):
    try:
        # Wrap file in formdata so it includes filename
        body = {"image": file}
        data = {}
        
        if overwrite:
            data["overwrite"] = "true"
  
        if subfolder:
            data["subfolder"] = subfolder

        resp = requests.post(f"http://{server_address}/upload/image", files=body,data=data)
        
        if resp.status_code == 200:
            data = resp.json()
            # Add the file to the dropdown list and update the widget value
            path = data["name"]
            if "subfolder" in data:
                if data["subfolder"] != "":
                    path = data["subfolder"] + "/" + path
            

        else:
            print(f"{resp.status_code} - {resp.reason}")
    except Exception as error:
        print(error)
    return path

def get_model_response(user_prompt, system_prompt):
    # NOTE: No f string and no whitespace in curly braces
    template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        {system_prompt}
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

    # Added prompt template
    prompt = PromptTemplate(
        input_variables=["system_prompt", "user_prompt"],
        template=template
    )
    
    # Modified invoking the model
    response = llm(prompt.format(system_prompt=system_prompt, user_prompt=user_prompt))
    
    return response

posts = 0

while True:
    os.startfile(r"C:\Users\Aech\Documents\Auto Insta\ComfyUI_windows_portable\run_nvidia_gpu.bat")
    server_address = "127.0.0.1:8188"
    client_id = str(uuid.uuid4())
    time.sleep(30)
    file = open(r"C:\Users\Aech\Documents\Auto Insta\cars.txt")
    cars = file.readlines()
    car = random.choice(cars)
    art_type = ["render", "fresco", "collage", "mosaic", "pastel drawing", "painting", "photograph", "oil painting", "watercolour painting", "cinematic photograph", "manga sketch", "digital artpiece", "detailed painting", "abstract painting"]
    artist = ["in the style of Chris Rahn", "in the style of Noah Bradley", "in the style of Caspar David Friedrich", "in the style of John Howe", "in the style of Greg Rutowski", "in a cyber punk style", "in a cartoon style", "in the style of Vincent Van Gogh", "in the style of Agnes Lawrence Pelton", "in the style of Alena Aenami", "in the style of Alex Grey", "in the style of Alfred Parsons", "in the style of Alice Neels", "in the style of Anton Fadeev", "in the style of Artgerm", "in the style of Bjarke Ingels", "in the style of Cristopher Balaskas", "in the style of Dan Mumford", "in the style of Dan Flavin", "in the style of Don Bluth", "in the style of Wes Anderson", "in the style of Felix Kelly", "in the style of Frederic Church", "in the style of John Atkinson Grimshaw", "in the style of Henry Ossawa Tanner", "in the style of Hiromu Arakawa", "in the style of Ilya Kuvshinov", "in the style of Jacob Hashimoto", "in the style of James Gilleard", "in the style of J.C.Leyendecker", "in the style of Jeff Koons", "in the style of Jeremy Mann", "in the style of Joe Jusko", "in the style of John Harris", "in the style of Jon Klassen", "in the style of Josan Gonzalez", "in the style of Kaethe Butcher", "in the style of Kay Sage", "in the style of Kazimir Malevich", "in the style of Kilian Eng", "in the style of Laurie Greasley", "in the style of Larry Elmore", "in the style of Leiji Masumoto", "in the style of Makoto Shinkai", "in the style of Marius Borgeaud", "in the style of Martiros Saryan", "in the style of Martine Johanna", "in the style of Mat Collishaw", "in the style of Matt Groening", "in the style of Maxfield Parrish", "in the style of Miho Hirano", "in the style of Beeple", "in the style of Georgia O'Keeffe", "in the style of Pablo Picasso", "in the style of Pamela Coleman Smith", "in the style of Patrick Brown", "in the style of Paul Gustave Fischer", "in the style of Paul Ranson",  "in the style of Pierre Bonanrd",  "in the style of Ralph McQuarrie", "in the style of RHADS", "in the style of Russ Mills", "in the style of Scott Listfield", "in the style of Satoshi Kon", "in the style of Shepard Fairey", "in the style of Shotaro Ishinomori", "in the style of Syd Mead", "in the style of Tatsuro Kouchi", "in the style of Tomer Hanuka", "in the style of Tyler Edlin", "in the style of Victo Ngai", "in the style of Vincent Di Fate", "in the style of Walt Disney", "in the style of William Blake", "in the style of William Gropper", "in the style of Scott Christian Sava", "in the style of Zaha Hadid"] 
    proposition = ["set in", "speeding through", "drifting through", "cruising through"]
    setting = ["Neo tokyo", "Medieval London", "New York", "a city in a dystopian future", "a village in a dystopian future", "a city in a utopian future", "a village in a utopian future", "a village in the dark times", "the barren landscape of Mars", "the barren landscape of the Moon", "the lush green landscape of the Amazon", "the dusty surface of Saturns rings", "Gotham City", "a big garage filled with 10 to 20 supercars", "a small home garage", "the himalayas", "the rocky mountains", "the beach side at sunset", "the beach side at sunrise", "the grand canyon", "the sahara desert", "the amazon forest", "the twisting roads of a mountain drive", "the cliffs of norway", "the black beaches of Iceland", "the rocky shores", "a drift rally", "a lush green meadow"]  
    additional = ["abstract", "matte", "3D", "photorealistic", "hyperrealistic", "bold", "vibrant", "noir", "neon", "cool colours" , "warm colours", "rainy", "sunny", "trending on ArtStation", "DeviantArt"]
    prompt = "A {} of a {} (car) {}, {} {}, {}".format(random.choice(art_type), car, random.choice(artist), random.choice(proposition), random.choice(setting), random.choice(additional))

    print("Prompt Generated:")
    print(prompt)

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
    llm = Ollama(model="llama3", stop=["<|eot_id|>"]) 

    #upload an image
    #with open("example.png", "rb") as f:
    #    comfyui_path_image = upload_file(f,"",True)

    #load workflow from file
    with open(r"C:\Users\Aech\Documents\Auto Insta\workflow.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    #set the text prompt for our positive CLIPTextEncode
    workflow["2"]["inputs"]["text_g"] = workflow["2"]["inputs"]["text_l"] = workflow["12"]["inputs"]["text_g"] = workflow["12"]["inputs"]["text_l"] = prompt
    workflow["5"]["inputs"]["text_g"] = workflow["5"]["inputs"]["text_l"] = workflow["13"]["inputs"]["text_g"] = workflow["13"]["inputs"]["text_l"] = "lowres, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry , deformed, random seed, signature, sign, autograph, naked, nudity, disfigurement, extra fingers, bad hands, hairiness, ugly, missing wheels, a lack of a car"

    seed = random.randint(1, 1000000000)
    #set the seed for our KSampler node
    workflow["7"]["inputs"]["seed"] = workflow["16"]["inputs"]["seed"] = seed

    #set the image name for our LoadImage node
    #workflow["10"]["inputs"]["image"] = comfyui_path_image

    #set model
    #workflow["14"]["inputs"]["ckpt_name"] = "meinamix_meinaV11.safetensors"
    
    images = get_images(ws, workflow)

    print("Image Generated.")
    #Commented out code to display the output images:

    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            #image.show()
            #save image
            image.save(r"C:\Users\Aech\Documents\Auto Insta\PaintingsCarsNew\{}-{}.png".format(node_id,seed))

    caption = get_model_response("A brief description of the {} and a short note on it's history".format(car),"Concise, with no coversational words.")
          
    brand = car.split()[0]
    brand = brand.lower()

    hashtag_list = [f"#{brand}","#cars","#art","#carporn","#aiart","#digitalart","#carart","#carsofinstagram","#carswithoutlimits","#carstagram","#sportcars","#artist","#artgallery","#artlover","#instaart","#contemporaryart","#streetart","#ai","#aiart","#aiartcommunity"]
    random.shuffle(hashtag_list)
    dots = random.randint(5,10)
    hashtags = ""

    for i in range(dots):
        hashtags += ". \n"

    for i in hashtag_list:
        hashtags += i
        hashtags += " "     
    
    caption += hashtags
    print(caption)
    
    auto.click(131,5) #Insta tab
    time.sleep(2)
    auto.moveTo(random.randint(16,227),random.randint(564,607)) #Create button
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(592,754),random.randint(499,523)) #Select button
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(182,284),random.randint(104,217)) #File select
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(748,834),random.randint(494,517)) #Open button
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(834,838),random.randint(229,231)) #Next button
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(1007,1011),random.randint(229,231)) #Next button
    auto.click()
    time.sleep(5)
    auto.moveTo(random.randint(700,1013),random.randint(313,478)) #Text box
    auto.click()
    time.sleep(3)
    auto.write(caption)
    time.sleep(2)
    auto.moveTo(random.randint(1007,1011),random.randint(229,231)) #Share button
    auto.click()
    time.sleep(2)
    auto.moveTo(random.randint(1319,1323),random.randint(146,150)) #Exit button
    auto.click()
    print("Posted!")
    posts += 1
    
    if os.path.exists(r"C:\Users\Aech\Documents\Auto Insta\PaintingsCarsNew\{}-{}.png".format(node_id,seed)):  
        os.remove(r"C:\Users\Aech\Documents\Auto Insta\PaintingsCarsNew\{}-{}.png".format(node_id,seed))
    else:
        print("File non existent")

    ws.close()
    os.system("taskkill /IM cmd.exe")
    print("POSTS: ",posts)
    time.sleep(random.randint(400,600))
