from pathlib import Path
from urllib.request import urlopen
import shutil
import sys
 
MODEL_URL = (
    "https://github.com/prabin466/Croc_Detection_System"
    "/releases/download/v1.0/croc_yolov8n.pt"
)
DEST = Path(__file__).parent / "models" / "croc_yolov8n.pt"
 
 
def download() -> None:
    if DEST.exists():
        print(f"Model already present at {DEST}")
        return
 
    DEST.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading from {MODEL_URL} ...")
 
    try:
        with urlopen(MODEL_URL) as response, open(DEST, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as error:
        DEST.unlink(missing_ok=True)  # don't leave a half-written file
        print(f"Download failed: {error}", file=sys.stderr)
        sys.exit(1)
 
    print(f"Saved to {DEST}")
 
 
if __name__ == "__main__":
    download()
  