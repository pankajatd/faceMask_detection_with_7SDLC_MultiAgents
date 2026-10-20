import os
import sys
import urllib.request
import cv2

sys.path.insert(0, r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection")
from src.detector import load_face_detector, detect_and_classify_frame
from src.utils import convert_rgb_to_bgr

test_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\tests\test_images"
output_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\output"

url = "https://raw.githubusercontent.com/prajnasb/observations/master/experiements/data/with_mask/11-with-mask.jpg"
in_path = os.path.join(test_dir, "dark_blue_mask_person.jpg")
out_path = os.path.join(output_dir, "result_dark_blue_mask_person.jpg")

# 1. Download dark blue mask image
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp, open(in_path, "wb") as f:
    f.write(resp.read())

print(f"1. Downloaded Dark Blue Mask Test Photo: {in_path}")

# 2. Run detection pipeline
img_bgr = cv2.imread(in_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

detector = load_face_detector(model_dir=r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\models")
result = detect_and_classify_frame(img_rgb, detector=detector)

annotated_bgr = convert_rgb_to_bgr(result["annotated_image"])
cv2.imwrite(out_path, annotated_bgr)

total = result["total_faces"]
masked = result["masked_count"]
unmasked = result["unmasked_count"]
details = result["results"]

print("\n" + "="*55)
print("TEST RESULT: DARK BLUE / NAVY MASK")
print(f"  Faces Located        : {total}")
print(f"  Masked (Green Box)   : {masked}")
print(f"  Unmasked (Red Box)   : {unmasked}")
for idx, d in enumerate(details, 1):
    lbl = d["label"]
    conf = d["confidence"] * 100
    box = d["box"]
    print(f"  Detection #{idx}      : {lbl} ({conf:.1f}%) at Box={box}")
print(f"  Annotated Image Saved: {out_path}")
print("="*55)
