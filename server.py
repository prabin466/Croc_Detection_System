import cv2
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from croc_detector.frame_processor import StreamExtractor
from croc_detector.pipeline import process_file
from croc_detector.annotator import annotator
from croc_detector.validation import validate_source, InvalidSourceError


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