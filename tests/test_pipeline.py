import pytest
from croc_detector.pipeline import get_extractor
from croc_detector.frame_processor import ImageExtractor, VideoExtractor


def test_video_extension():
    assert isinstance(get_extractor("video.avi"), VideoExtractor)
    assert isinstance(get_extractor("video.mov"), VideoExtractor)
    assert isinstance(get_extractor("video.mp4"), VideoExtractor)

def test_image_extension():
    assert isinstance(get_extractor("image.jpeg"), ImageExtractor)
    assert isinstance(get_extractor("image.png"), ImageExtractor)
    assert isinstance(get_extractor("image.jpg"), ImageExtractor) 

def test_unsupported_extension():
    with pytest.raises(ValueError):
        get_extractor("document.pdf")

    with pytest.raises(ValueError):
        get_extractor("document.docx")

