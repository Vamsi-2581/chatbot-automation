import pyautogui
import time
from Vision import VNImageRequestHandler, VNRecognizeTextRequest
from Foundation import NSDictionary
import Quartz
import Vision
from Cocoa import NSURL
from wurlitzer import pipes 
import re





time.sleep(5)

left = 552
top = 188
right = 1441
bottom = 793

width = right - left
height = bottom - top

def take_screenshot():
    img = pyautogui.screenshot(region=(left, top, width, height))
    img.save("chat.png")

print("Screenshot Saved")

def imagetotext(img_path,lang="eng"):
    input_url= NSURL.fileURLWithPath_(img_path)
    
    with pipes() as (out,err):
        
        input_image= Quartz.CIImage.imageWithContentsOfURL_(input_url)
        
    vision_options= NSDictionary.dictionaryWithDictionary_({})
    vision_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
        input_image,vision_options
    )
    
    results=[]
    handler=make_request_handler(results)
    vision_request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(handler)
    
    error = vision_handler.performRequests_error_([vision_request], None)
    
    return results


def make_request_handler(results):
    """ results: list to store results """
    if not isinstance(results, list):
        raise ValueError("results must be a list")

    def handler(request, error):
        if error:
            print(f"Error! {error}")
        else:
            observations = request.results()
            for text_observation in observations:
                recognized_text = text_observation.topCandidates_(1)[0]
                bbox=text_observation.boundingBox()
                
                results.append([recognized_text.string(),
                                recognized_text.confidence(),
                                bbox.origin.x,
                                bbox.origin.y])
    return handler

def is_time(text):
    pattern = r"^\d{1,2}:\d{2}\s?(am|pm)$"
    return re.match(pattern, text.lower()) is not None

def clean_text(text):
    text = re.sub(r"\d{1,2}:\d{2}\s?(am|pm)", "", text, flags=re.I)
    text = re.sub(r"[/]+", "", text)
    return text.strip()

last_processed_message = None

def process_results(results):
    
    global last_processed_message
    
    results.sort(
        key= lambda item: item[3],
        reverse=True
    )
    
    conversation=[]

    for item in results:
       
        text = item[0]
        confidence = item[1]
        x = item[2]
        y = item[3]
        if is_time(text):
            continue
        
        text=clean_text(text)
        if not text:
            continue
            
        
        if x < 0.5:
            conversation.append({
                "role":"received",
                "text":text
            })
        else:
            conversation.append({
                "role":"sent",
                "text":text
            })
    
    for msg in conversation:
        print(msg)
        
    latest_message = None
        
    for msg in reversed(conversation):
        if msg["role"] == "received":
            latest_message = msg
            break
        
    if latest_message is None:
        print("No received message found")
        return
    
    latest_text = latest_message["text"]

    if latest_text == last_processed_message:
        print("Already processed")
        return

    last_processed_message = latest_text
        
    
    def get_reply(message):
        if "kaha" in message.lower():
            return "Room me hu"
        
        if "aa" in message.lower():
            return "Aa raha hu"

        return "Okay"
    
    print("Latest message:", latest_message)
    
    print("before reply")
    reply = get_reply(latest_message["text"])
    print("reply:" ,reply)
    time.sleep(2)
    pyautogui.click(665, 831)
    time.sleep(0.5)
    pyautogui.write(reply, interval=0.05)
    pyautogui.press("enter")
    

        

            
            
while True:
    print("Checking messages...")

    take_screenshot()

    results = imagetotext("chat.png")
    process_results(results)

    time.sleep(5)




