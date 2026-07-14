from croc_detector.frame_processor import StreamExtractor
from unittest.mock import patch, MagicMock
import pytest


def test_start_stream_raises_on_bad_source():
    extractor = StreamExtractor()
    fake_cap = MagicMock()
    fake_cap.isOpened.return_value = False
    with patch('croc_detector.frame_processor.cv2.VideoCapture', return_value=fake_cap):
        with pytest.raises(ValueError):
            extractor.start_stream("bad_source")

    fake_cap.release.assert_called_once()