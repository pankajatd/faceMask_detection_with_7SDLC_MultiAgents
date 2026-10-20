import os
import sys
sys.path.insert(0, os.path.abspath("."))
import cv2
import shutil
import numpy as np
from src.detector import load_face_detector, detect_and_classify_frame, classify_mask_region

user_dir = r"C:\Users\panka\.gemini\antigravity\brain\ce6e92d6-586e-4366-aa56-1c9b40d5054a\.user_uploaded"
out_dir = r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\output\user_uploads"
art_dir = r"C:\Users\panka\.gemini\antigravity\brain\ce6e92d6-586e-4366-aa56-1c9b40d5054a"
os.makedirs(out_dir, exist_ok=True)

test_files = [
    ("doctor_blue_scrubs.jpg", "media_1792498666518_a41293b7.jpg"),
    ("medical_team.jpg", "media_1792498666518_89d0f4e8.jpg"),
    ("two_nurses_gloves.jpg", "media_1792498666519_5b2c3dac.jpg"),
    ("side_profile_black_mask.jpg", "media_1792498666557_2d078eb2.jpg")
]

detector = load_face_detector("models")
print("Detector type:", detector.model_type)

for alias, fname in test_files:
    fpath = os.path.join(user_dir, fname)
    bgr = cv2.imread(fpath)
    if bgr is None:
        print("Could not load:", fpath)
        continue
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    res = detect_and_classify_frame(rgb, detector)
    
    print("\n" + "=" * 50)
    print(f"Image: {alias} ({fname})")
    print(f"Dimensions: {rgb.shape[1]}x{rgb.shape[0]}")
    print(f"Total Faces: {res['total_faces']}, Masked: {res['masked_count']}, Unmasked: {res['unmasked_count']}")
    
    for i, r in enumerate(res['results']):
        sX, sY, eX, eY = r['box']
        face_roi = rgb[sY:eY, sX:eX]
        fh, fw = face_roi.shape[:2]
        mouth_roi = face_roi[int(fh * 0.55):int(fh * 0.92), int(fw * 0.20):int(fw * 0.80)]
        if mouth_roi.size > 0:
            r_m, g_m, b_m = np.mean(mouth_roi, axis=(0, 1))
            mean_b = (r_m + g_m + b_m) / 3.0
            std_m = float(np.mean(np.std(mouth_roi, axis=(0, 1))))
        else:
            r_m, g_m, b_m, mean_b, std_m = 0, 0, 0, 0, 0
        print(f"  Face #{i+1}: Box={r['box']}, Label={r['label']}, Conf={r['confidence']:.2f}")
        print(f"           Color metrics: R={r_m:.1f}, G={g_m:.1f}, B={b_m:.1f}, Brightness={mean_b:.1f}, Std={std_m:.1f}")
        
    out_bgr = cv2.cvtColor(res['annotated_image'], cv2.COLOR_RGB2BGR)
    save_path = os.path.join(out_dir, f"tested_{alias}")
    cv2.imwrite(save_path, out_bgr)
    
    art_path = os.path.join(art_dir, f"tested_{alias}")
    cv2.imwrite(art_path, out_bgr)
    print(f"  Saved visual output to: {save_path}")
