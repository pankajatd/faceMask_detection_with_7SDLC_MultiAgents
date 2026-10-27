# Product Requirements Document (PRD)
## Project: Face Mask Detection System (`faceMask_detection`)
**Author:** Product Manager Subagent  
**Status:** DRAFT FOR HITL GATE 1 REVIEW  
**Scope:** Business Goals, User Stories & Screen Features  

---

## 1. Executive Summary & Problem Statement
In healthcare centers, corporate offices, airports, and public facilities, maintaining health and safety standards requires ensuring that visitors and staff wear face masks properly. Relying on staff to manually check every person is stressful, slow, and prone to human error.

The **`faceMask_detection`** product solves this by providing a simple, automated web dashboard that allows safety officers and administrators to:
1. Upload photos to instantly check if individuals are wearing masks.
2. Monitor entrances via live camera feeds.
3. Clearly see who is compliant (Green alert) and who is not (Red alert).

---

## 2. Target Users & Personas

| User Persona | Role | What They Care About Most |
| :--- | :--- | :--- |
| **Front Desk / Security Staff** | Screens visitors at building entrances | Needs fast, visual alerts so they can spot non-compliant visitors without delay. |
| **Safety & Compliance Manager** | Reviews safety records and photos | Needs to upload photos from surveillance cameras and see compliance statistics. |
| **Non-Technical Staff** | Uses the tool daily | Needs a clean, friendly web screen with no complicated setup or technical commands. |

---

## 3. User Stories (The Human Perspective)

* **Story 1 (Photo Upload & Instant Check)**:
  * *As a* Safety Manager,
  * *I want to* drag and drop photos of people into the web page,
  * *So that* the system highlights everyone with or without a mask immediately.

* **Story 2 (Live Camera Monitoring)**:
  * *As a* Front Desk Security Guard,
  * *I want to* turn on the camera feed at the entrance,
  * *So that* I can monitor visitors walking in without having to stop them.

* **Story 3 (Visual Clarity & Alert Colors)**:
  * *As a* Security Guard,
  * *I want to* see obvious colors (Green for compliant, Red for non-compliant) around faces,
  * *So that* I don't have to read tiny text or guess who is wearing a mask.

* **Story 4 (Sensitivity Adjustment)**:
  * *As an* Auditor,
  * *I want to* adjust a sensitivity slider on the screen,
  * *So that* I can tune how strict the detection should be for dim or bright lighting.

* **Story 5 (Saving Reports)**:
  * *As a* Safety Manager,
  * *I want to* download the marked image with the boxes,
  * *So that* I can save it as proof for our weekly safety audit records.

---

## 4. Product Features (What the User Sees and Uses on Screen)

### 4.1 Mask Detection & Visual Feedback
* **Feature 1**: The application must locate human faces in uploaded pictures or camera streams.
* **Feature 2**: For each face found, the application classifies:
  * **`Mask`**: The person is properly wearing a face mask covering mouth and nose.
  * **`No Mask`**: The person is not wearing a mask or has pulled it down.
* **Feature 3**: The application draws colored boxes around each face:
  * **Green Box** around faces with a mask.
  * **Red Box** around faces without a mask.
* **Feature 4**: The box displays a clear label and percentage (e.g., `Mask: 98%`, `No Mask: 95%`).

### 4.2 Web Dashboard Interface
* **Feature 5 (Navigation)**: Provide a clean sidebar allowing the user to switch between:
  1. **Upload Photo Mode**
  2. **Live Camera Mode**
* **Feature 6 (Photo Uploading)**: Provide a drag-and-drop box for photo files (`.jpg`, `.jpeg`, `.png`).
* **Feature 7 (Sensitivity Control)**: Provide a slider labeled **"Detection Confidence Threshold"** (ranging from 50% to 95%) so the user can easily adjust detection strictness.
* **Feature 8 (Summary Counters)**: Display three clear counter cards beneath the image:
  * **Total Faces Detected**
  * **Masked Faces (Compliant)**
  * **Unmasked Faces (Needs Attention)**
* **Feature 9 (Save Feature)**: Provide a **"Download Annotated Image"** button so the user can save the marked photo to their computer.

---

## 5. Non-Functional User Expectations

* **Usability**: The dashboard must be intuitive enough for a non-technical person to use without training.
* **Speed**: When a user drops an image, the result should appear on the screen in less than 2 seconds.
* **Clarity**: Text and colors must be high-contrast and readable on standard monitors and laptops.

---

## 6. Business Acceptance Criteria

This product will be considered successfully delivered when:
- [ ] A user can open the dashboard in a web browser.
- [ ] Uploading a photo of a person wearing a mask displays a **Green box** labeled **"Mask"**.
- [ ] Uploading a photo of a person with a bare face displays a **Red box** labeled **"No Mask"**.
- [ ] Uploading a group photo with multiple people highlights each face correctly.
- [ ] The summary counter accurately counts total masked and unmasked individuals.
- [ ] The user can click "Download" and receive the resulting marked image.
