import os
import sys
import urllib.request
import cv2

sys.path.insert(0, r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection")

from src.detector import load_face_detector, detect_and_classify_frame
from src.utils import convert_rgb_to_bgr

test_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\tests\test_images"
output_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\output"
os.makedirs(test_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Standard face mask benchmark sample images
urls = {
    "person_with_mask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/with_mask/0-with-mask.jpg",
    "person_no_mask.jpg": "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/without_mask/0.jpg",
    "sample_face.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"
}

print("1. Downloading verified test images...")
for fname, url in urls.items():
    fpath = os.path.join(test_dir, fname)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp, open(fpath, "wb") as out_f:
            out_f.write(resp.read())
        print(f"   Downloaded: {fname} ({os.path.getsize(fpath)} bytes)")
    except Exception as e:
        print(f"   Failed downloading {fname}: {e}")

print("\n2. Initializing AI Detector (ResNet-10 SSD Deep Learning)...")
detector = load_face_detector(model_dir=r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\models")
print(f"   Active Model Type: {detector.model_type}")

print("\n3. Running Detection & Classification on All Test Images...")
for fname in sorted(os.listdir(test_dir)):
    if fname.lower().endswith((".jpg", ".png", ".jpeg")):
        in_path = os.path.join(test_dir, fname)
        img_bgr = cv2.imread(in_path)
        if img_bgr is None:
            continue

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Execute detection pipeline
        result = detect_and_classify_frame(img_rgb, detector=detector, confidence_threshold=0.60)
        
        # Save output image with Green/Red boxes drawn
        out_fname = "result_" + fname
        out_path = os.path.join(output_dir, out_fname)
        
        annotated_bgr = convert_rgb_to_bgr(result["annotated_image"])
        cv2.imwrite(out_path, annotated_bgr)
        
        total = result["total_faces"]
        masked = result["masked_count"]
        unmasked = result["unmasked_count"]
        details = result["results"]
        
        print("\n" + "="*50)
        print(f"TEST IMAGE: {fname}")
        print(f"  Total Faces Located : {total}")
        print(f"  Masked Faces (Green): {masked}")
        print(f"  Unmasked Faces (Red): {unmasked}")
        for idx, det in enumerate(details, 1):
            print(f"  Detection #{idx}: Label='{det['label']}', Confidence={det['confidence']*100:.1f}%, Box={det['box']}")
        print(f"  Output Image Saved  : {out_path}")

print("\n" + "="*50)
print("TEST COMPLETED: All output images with Green and Red boxes are saved in:")
print(output_dir)
