import os
import sys
import urllib.request
import cv2

sys.path.insert(0, r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection")
from src.detector import load_face_detector, detect_and_classify_frame
from src.utils import convert_rgb_to_bgr

diverse_test_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\tests\test_images\diverse_tests"
diverse_out_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\output\diverse_tests"

os.makedirs(diverse_test_dir, exist_ok=True)
os.makedirs(diverse_out_dir, exist_ok=True)

# 7 completely distinct real-world photos
image_urls = {
    "1_female_blue_surgical_mask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/with_mask/1-with-mask.jpg",
    "2_male_white_n95_mask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/with_mask/4-with-mask.jpg",
    "3_person_black_mask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/with_mask/10-with-mask.jpg",
    "4_person_bare_face_male.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/without_mask/1.jpg",
    "5_person_bare_face_female.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/without_mask/3.jpg",
    "6_person_tilted_head_nomask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/without_mask/10.jpg",
    "7_athlete_action_nomask.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg"
}

print("1. Downloading 7 Completely Different Real-World Images...")
for fname, url in image_urls.items():
    fpath = os.path.join(diverse_test_dir, fname)
    if not os.path.exists(fpath):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp, open(fpath, "wb") as f:
            f.write(resp.read())
        print(f"   Downloaded: {fname}")
    else:
        print(f"   Already exists: {fname}")

print("\n2. Initializing AI Detector (ResNet-10 SSD)...")
detector = load_face_detector(model_dir=r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\models")

print("\n3. Testing All 7 Different Images...")
for fname in sorted(os.listdir(diverse_test_dir)):
    if fname.lower().endswith((".jpg", ".png", ".jpeg")):
        in_path = os.path.join(diverse_test_dir, fname)
        img_bgr = cv2.imread(in_path)
        if img_bgr is None:
            continue
            
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        result = detect_and_classify_frame(img_rgb, detector=detector, confidence_threshold=0.50)
        
        out_path = os.path.join(diverse_out_dir, "result_" + fname)
        annotated_bgr = convert_rgb_to_bgr(result["annotated_image"])
        cv2.imwrite(out_path, annotated_bgr)
        
        total = result["total_faces"]
        masked = result["masked_count"]
        unmasked = result["unmasked_count"]
        details = result["results"]
        
        print("\n" + "="*55)
        print(f"IMAGE: {fname}")
        print(f"  Faces Located : {total}")
        print(f"  Masked (Green): {masked}")
        print(f"  Unmasked (Red): {unmasked}")
        for idx, d in enumerate(details, 1):
            lbl = d["label"]
            conf = d["confidence"] * 100
            print(f"  Detection #{idx}: {lbl} ({conf:.1f}%)")
        print(f"  Saved to: {out_path}")

print("\nAll 7 diverse image tests finished successfully!")
