# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 00:29:25 2023

@author: ThibautR
"""
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
import cv2
from diffusers import StableDiffusionInpaintPipeline
import torch
import matplotlib.pyplot as plt
from PIL import Image

def maskCreator(image, prompt):
    processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
    model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")
    prompts = [prompt, prompt, prompt, prompt]
    inputs = processor(text=prompts, images=[image] * len(prompts), padding="max_length", return_tensors="pt")
    
    # predict
    with torch.no_grad():
      outputs = model(**inputs)
    
    preds = outputs.logits.unsqueeze(1)
    filename = "mask.png"

    # here we save the second mask
    plt.imsave(filename,torch.sigmoid(preds[0][0]))
    img2 = cv2.imread(filename)
    
    gray_image = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (thresh, bw_image) = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    # fix color format
    cv2.cvtColor(bw_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(bw_image)

def inPainting(image, bw_image, prompt):
    im_orig_size=image.size
    bw_resized = bw_image.resize((512,512))
    image_resized = image.resize((512,512))
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-inpainting",
    torch_dtype=torch.float32,
    )
    #image and mask_image should be PIL images.
    #The mask structure is white for inpainting and black for keeping as is
    image_result = pipe(prompt=prompt, image=image_resized, mask_image=bw_resized).images[0]
    return image_result.resize(im_orig_size)

def fullTreatment(image,prompt_mask,prompt_painting):
    return inPainting(image,maskCreator(image, prompt_mask),prompt_painting)