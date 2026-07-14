import threading

from croc_detector.frame_processor import StreamExtractor
from unittest.mock import patch, MagicMock
from itertools import chain, repeat
import pytest
import numpy as np


def test_start_stream_raises_on_bad_source():
    extractor = StreamExtractor()
    fake_cap = MagicMock()
    fake_cap.isOpened.return_value = False
    with patch('croc_detector.frame_processor.cv2.VideoCapture', return_value=fake_cap):
        with pytest.raises(ValueError):
            extractor.start_stream("bad_source")
    fake_cap.release.assert_called_once()


def test_extract_does_not_yield_duplicate_frames():
    frame_a = np.full((480, 640, 3),1,  dtype=np.uint8)
    frame_b = np.full((480, 640, 3),  2, dtype=np.uint8)
    frame_c = np.full((480, 640, 3), 3, dtype=np.uint8)

    fake_cap = MagicMock()
    fake_cap.isOpened.return_value = True

    fake_cap.read.side_effect = chain(
        [(True, frame_a), (True, frame_a), (True, frame_b), (True, frame_b), (True, frame_c)],
        repeat((False, None)))

    with patch('croc_detector.frame_processor.cv2.VideoCapture', return_value=fake_cap):
        extractor = StreamExtractor()
        frames = []
        gen = extractor.extract("fake_source")
        stopper = threading.Timer(0.5,extractor.stop_stream)
        stopper.start()
        for frame in gen:
            frames.append(frame)

    assert len(frames) > 0
    assert len(frames) == len({f.tobytes() for f in frames})

