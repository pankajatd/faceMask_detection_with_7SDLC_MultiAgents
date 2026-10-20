import os
import sys
import cv2
import numpy as np

sys.path.insert(0, r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection")
from src.detector import load_face_detector, detect_and_classify_frame
from src.utils import convert_rgb_to_bgr

test_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\tests\test_images"
output_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\output"

# Clean up debug crop
debug_crop = os.path.join(output_dir, "crop_masked.jpg")
if os.path.exists(debug_crop):
    os.remove(debug_crop)

# Load existing base images
img_mask = cv2.imread(os.path.join(test_dir, "person_with_mask.jpg"))
img_nomask = cv2.imread(os.path.join(test_dir, "person_no_mask.jpg"))

print("1. Creating Realistic Edge-Case Test Images...")

# --- EDGE CASE 1: Tilted Face (25-degree rotation) ---
h, w = img_nomask.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 25, 1.0)
tilted_face = cv2.warpAffine(img_nomask, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite(os.path.join(test_dir, "edge_1_tilted_face.jpg"), tilted_face)
print("   Created: edge_1_tilted_face.jpg (25-degree head tilt)")

# --- EDGE CASE 2: Blurry Image (Simulating low-quality CCTV) ---
blurry_face = cv2.GaussianBlur(img_mask, (21, 21), 0)
cv2.imwrite(os.path.join(test_dir, "edge_2_blurry_cctv.jpg"), blurry_face)
print("   Created: edge_2_blurry_cctv.jpg (Simulated heavy CCTV camera blur)")

# --- EDGE CASE 3: Boundary Condition (Face Clipped at Border) ---
boundary_img = np.zeros((400, 400, 3), dtype=np.uint8) + 120
crop_part = img_nomask[:200, :150]
boundary_img[0:crop_part.shape[0], 0:crop_part.shape[1]] = crop_part
cv2.imwrite(os.path.join(test_dir, "edge_3_boundary_clipped.jpg"), boundary_img)
print("   Created: edge_3_boundary_clipped.jpg (Face clipped at image border x=0, y=0)")

# --- EDGE CASE 4: Multi-Person Group Photo (Masked + Unmasked together) ---
h_target = 350
w_mask = int(img_mask.shape[1] * (h_target / img_mask.shape[0]))
w_nomask = int(img_nomask.shape[1] * (h_target / img_nomask.shape[0]))

res_mask = cv2.resize(img_mask, (w_mask, h_target))
res_nomask = cv2.resize(img_nomask, (w_nomask, h_target))
group_img = np.hstack([res_mask, res_nomask])
cv2.imwrite(os.path.join(test_dir, "edge_4_multi_person_group.jpg"), group_img)
print("   Created: edge_4_multi_person_group.jpg (Masked + Unmasked people side-by-side)")

print("\n2. Initializing AI Detector (ResNet-10 SSD)...")
detector = load_face_detector(model_dir=r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\models")
print(f"   Active Model Type: {detector.model_type}")

print("\n3. Running Detection Pipeline on Edge Cases...")
edge_files = [
    "edge_1_tilted_face.jpg",
    "edge_2_blurry_cctv.jpg",
    "edge_3_boundary_clipped.jpg",
    "edge_4_multi_person_group.jpg"
]

for fname in edge_files:
    in_path = os.path.join(test_dir, fname)
    img_bgr = cv2.imread(in_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    result = detect_and_classify_frame(img_rgb, detector=detector, confidence_threshold=0.50)
    
    out_path = os.path.join(output_dir, "result_" + fname)
    annotated_bgr = convert_rgb_to_bgr(result["annotated_image"])
    cv2.imwrite(out_path, annotated_bgr)
    
    total = result["total_faces"]
    masked = result["masked_count"]
    unmasked = result["unmasked_count"]
    details = result["results"]
    
    print("\n" + "="*55)
    print(f"TEST: {fname}")
    print(f"  Faces Located : {total}")
    print(f"  Masked (Green): {masked}")
    print(f"  Unmasked (Red): {unmasked}")
    for idx, d in enumerate(details, 1):
        lbl = d["label"]
        conf = d["confidence"] * 100
        box = d["box"]
        print(f"  Detection #{idx}: {lbl} ({conf:.1f}%) at Box={box}")
    print(f"  Visual Output : {out_path}")

print("\n" + "="*55)
print("ALL EDGE CASE TESTS COMPLETED!")
