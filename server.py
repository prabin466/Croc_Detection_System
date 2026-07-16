import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from croc_detector.frame_processor import StreamExtractor
from croc_detector.pipeline import process_file
from croc_detector.annotator import annotator


app = FastAPI()

extractor = StreamExtractor()

def generate_frames(path):
    for frame, detection in process_file(path, extractor = extractor):
        annotated = annotator(frame, detection)
        ret, buffer = cv2.imencode('.jpg', annotated)
        if not ret:
            continue
        jpg = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')


@app.get("/stream")
def stream(path: str):
    return StreamingResponse(generate_frames(path),
                             media_type='multipart/x-mixed-replace; boundary=frame') 