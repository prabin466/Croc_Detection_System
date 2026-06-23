import cv2
import streamlit as st
from croc_detector.pipeline import process_file
from croc_detector.annotator import annotator
from croc_detector.config import SUPPORTED_IMAGES, SUPPORTED_VIDEOS, UPLOADS_DIR


st.title("Crocodile Detection System")

all_formats = SUPPORTED_IMAGES + SUPPORTED_VIDEOS
formats = [extn[1:] for extn in all_formats]
uploaded_file = st.file_uploader("Upload an Image or Video", type=formats)

if uploaded_file is not None:
    save_path = UPLOADS_DIR/uploaded_file.name
    if st.button("Detect Crocodiles"):
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        foundAny =  False
        for frame, detections in process_file(save_path):
             if detections:
                foundAny = True
                frame = annotator(frame, detections)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb)
        if not foundAny:
            st.write("No crocodiles detected.")
