import cv2
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from croc_detector.frame_processor import StreamExtractor, STREAM_TIMEOUT_SECONDS
from croc_detector.pipeline import process_file
from croc_detector.annotator import annotator
from croc_detector.validation import validate_source, InvalidSourceError
from croc_detector.config import STREAM_TIMEOUT_SECONDS


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
    try:
        validated_path = validate_source(path)
    except InvalidSourceError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StreamingResponse(generate_frames(validated_path),
                             media_type='multipart/x-mixed-replace; boundary=frame') 

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/stream/status")
def stream_status():
    frame, frame_id = extractor.get_latest_frame()
    with extractor.lock:
        last_frame_time = extractor.last_frame_time\

    if last_frame_time is None:
        age =  None
    else:
        age = time.time() - last_frame_time

    if not extractor.running:
        healthy = False
    elif age is None:
        healthy = False
    elif age > STREAM_TIMEOUT_SECONDS:
        healthy = False
    else:
        healthy = True

    return {
        "healthy" : healthy,
        "running" : extractor.running,
        "state" : extractor.state.value,
        "frame_id" : frame_id,
        "last_frame_age_seconds": age
    }

