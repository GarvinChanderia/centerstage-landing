#!/usr/bin/env python3
import requests, base64, sys, json
from datetime import datetime
from pathlib import Path
import time

API_KEY = "AIzaSyDtRkjcd9lqAjieE5sGRUJluvSCizsokJw"
MODEL   = "gemini-2.5-flash-image"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

prefix_model = "High-end luxury fashion editorial photography, 'Quiet Luxury' aesthetic. 35-year-old sophisticated Indian female model. High whitespace, dynamic still shot, editorial magazine framing. Focus on natural-origin fibers like pure silk, premium cotton, and breathable linen. Soft natural professional lighting. NO TEXT. NO TYPOGRAPHY. NO LOGOS. NO WATERMARKS. "
prefix_fabric = "High-end luxury fashion editorial macro photography, 'Quiet Luxury' aesthetic. Focus on natural-origin fibers like pure silk, premium cotton, and breathable linen. Soft natural professional lighting. NO TEXT. NO TYPOGRAPHY. NO LOGOS. NO WATERMARKS. "
prefix_other = "High-end luxury editorial photography, 'Quiet Luxury' aesthetic. Minimalist, sophisticated. Soft natural professional lighting. NO TEXT. NO TYPOGRAPHY. NO LOGOS. NO WATERMARKS. "

prompts = {
    # Existing Vogue set
    "vogue_hero_primary.png": prefix_model + "Model looking directly at the camera with quiet power. Wearing a sophisticated Soft Beige (hex #dac8b3) tailored linen button-down shirt. Minimalist modern office environment with subtle Muted Sage (hex #778176) accents.",
    "vogue_work_desk.png": prefix_model + "Model sitting at an elegant modern work desk, looking confidently at the camera. Wearing a sophisticated Dark Olive Green (hex #4d4f34) silk midi shirt dress. Natural sunlight.",
    "vogue_work_meeting.png": prefix_model + "Model in a sleek modern meeting room, looking at the camera. Wearing a tailored office-appropriate Mauve (hex #ad8e8c) cotton wrap-style top with Dusty Blue (hex #9fb3c0) background elements. Soft shadows.",
    "vogue_coffee_window.png": prefix_model + "Model sitting by a chic coffee shop window, holding a coffee cup and looking softly at the camera. Wearing a stylish Dusty Blue (hex #9fb3c0) linen button-down.",
    "vogue_travel_lounge.png": prefix_model + "Model in a luxury travel lounge, looking at the camera. Wearing comfortable but elegant Deep Burgundy (hex #590834) tailored travel wear.",
    "vogue_home_morning.png": prefix_model + "Model in a high-end minimalist home setting in the morning, looking gently at the camera. Wearing a soft, elegant Pale Mustard (hex #ffeb88) cotton button-down.",
    
    # Other Lifestyle
    "cs_evening_restaurant.png": prefix_model + "Model at an upscale evening restaurant, looking confidently at the camera. Wearing an elegant Burnt Sienna (hex #582e30) silk evening dress. Moody, sophisticated lighting.",
    "cs_about_ethos.png": prefix_model + "Model in motion, walking elegantly with purpose. Wearing a flowing Muted Sage (hex #778176) wrap dress. Minimalist architectural background.",
    "cs_brand_movement.png": prefix_model + "Model writing thoughtfully in a journal. Wearing a Dark Olive Green (hex #4d4f34) cotton button-down. Elegant, quiet luxury office setting.",
    "cs_founder_office.png": prefix_model + "Professional woman in a sophisticated minimalist office, confident and relaxed pose. Wearing a Deep Burgundy (hex #590834) tailored suit.",
    
    # Fabrics & Details
    "cs_fabric_texture_closeup.png": prefix_fabric + "Extreme macro close-up of premium Soft Beige (hex #dac8b3) linen fabric showing intricate weave pattern and soft morning light.",
    "cs_fabric_drape_study.png": prefix_fabric + "Drape study of premium silk fabric in Dusty Blue (hex #9fb3c0), light reflecting off the sheen, elegant folds.",
    "cs_macro_cotton.png": prefix_fabric + "Extreme macro of high quality cotton texture in Pale Mustard (hex #ffeb88), soft shadows, clean aesthetic.",
    "cs_draped_silk_rose.png": prefix_fabric + "Draped silk fabric in a Mauve (hex #ad8e8c) tone, elegant folds, soft studio lighting.",
    "cs_shoulder_padding.png": prefix_fabric + "Detailed view of a jacket shoulder with soft padding and precision stitching in Dark Olive Green (hex #4d4f34) against a neutral studio background.",
    "cs_trouser_pleats.png": prefix_fabric + "Mid-section of a high-waisted tailored trouser showing refined pleats and waist construction in Burnt Sienna (hex #582e30).",
    "cs_sleeve_cuff.png": prefix_fabric + "Close up of a shirt sleeve cuff and arm, demonstrating the drape of Muted Sage (hex #778176) fabric.",
    "cs_french_seam.png": prefix_fabric + "Interior view of a luxury garment showing a clean French seam and silk lining in Deep Burgundy (hex #590834).",
    "cs_zipper_button.png": prefix_fabric + "Close up of a custom metal button and brass zipper on premium Soft Beige (hex #dac8b3) fabric.",
    "cs_silk_lining.png": prefix_fabric + "Subtle texture of a fine silk lining fabric in Dusty Blue (hex #9fb3c0), ripples of light and shadow.",
    "cs_tailoring_hands.png": prefix_fabric + "Artisan tailor's hands working with high-end fabric in Mauve (hex #ad8e8c), needle and thread visible, professional studio lighting.",
    
    # Environment
    "cs_atelier_map.png": prefix_other + "Minimalist architectural line drawing of an urban grid in muted beige and charcoal tones.",
    "cs_minimalist_rack.png": prefix_other + "Minimalist boutique interior with curated premium clothing on a brass rack. Garments in shades of Mauve, Dusty Blue, and Soft Beige. Soft ambient lighting, airy atmosphere."
}

out_dir = Path("Center Stage assets/images")
out_dir.mkdir(parents=True, exist_ok=True)

for filename, prompt in prompts.items():
    output_path = out_dir / filename
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }
    print(f"Generating {filename}...", flush=True)
    try:
        r = requests.post(URL, json=payload, timeout=60)
        if r.status_code != 200:
            print(f"Failed {filename}: {r.status_code} {r.text}", flush=True)
            continue
        
        data = r.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            parts = data["candidates"][0]["content"]["parts"]
            found = False
            for part in parts:
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    output_path.write_bytes(img_bytes)
                    print(f"Saved: {output_path.resolve()} ({len(img_bytes):,} bytes)", flush=True)
                    found = True
                    break
            if not found:
                print(f"No image in response for {filename}:")
                # print(json.dumps(data, indent=2))
        else:
             print(f"No candidates in response for {filename}")
    except Exception as e:
        print(f"Error for {filename}: {e}", flush=True)
    time.sleep(2)
