import pytest
from croc_detector.validation import validate_source, InvalidSourceError


def test_public_ip_passes():
    assert validate_source("rtsp://8.8.8.8:554/feed") == "rtsp://8.8.8.8:554/feed"


def test_bad_scheme_rejected():
    with pytest.raises(InvalidSourceError):
        validate_source("file:///etc/passwd")


def test_loopback_rejected():
    with pytest.raises(InvalidSourceError):
        validate_source("http://127.0.0.1:8000/admin")


def test_link_local_metadata_rejected():
    with pytest.raises(InvalidSourceError):
        validate_source("http://169.254.169.254/")


def test_empty_rejected():
    with pytest.raises(InvalidSourceError):
        validate_source("")