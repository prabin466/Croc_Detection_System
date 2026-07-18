import cv2
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse

from croc_detector.frame_processor import StreamExtractor, STREAM_TIMEOUT_SECONDS
from croc_detector.pipeline import process_file
from croc_detector.annotator import annotator
from croc_detector.validation import validate_source, InvalidSourceError
from croc_detector.config import STREAM_TIMEOUT_SECONDS, STREAMLIT_URL, DEFAULT_STREAM_SOURCE


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

@app.get("/", response_class=HTMLResponse)
def landing():
    return f"""
    <html>
      <head><title>Crocodile Detection System</title></head>
      <body>
        <h1>Crocodile Detection System</h1>
        <p>Choose a mode:</p>
        <ul>
          <li><a href="/live">Live stream</a> — monitor an RTSP or HTTP camera feed</li>
          <li><a href="{STREAMLIT_URL}">Upload a file</a> — run detection on an image or video</li>
        </ul>
      </body>
    </html>
    """

@app.get("/live", response_class=HTMLResponse)
def live():
    return f"""
    <html>
      <head><title>Live Stream</title></head>
      <body>
        <h1>Live stream</h1>
        <form id="src-form">
          <input type="text" id="path" name="path" size="50"
                 value="{DEFAULT_STREAM_SOURCE}"
                 placeholder="rtsp://camera-host:8554/stream">
          <button type="submit">Start</button>
        </form>

        <img id="feed" width="800">

        <p><a href="/">Back</a></p>

        <script>
          document.getElementById('src-form').addEventListener('submit', (e) => {{
            e.preventDefault();
            const src = document.getElementById('path').value;
            document.getElementById('feed').src =
              '/stream?path=' + encodeURIComponent(src);
          }});
        </script>
      </body>
    </html>
    """