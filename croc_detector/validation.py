import ipaddress
import socket
from urllib.parse import urlparse

from croc_detector.config import ALLOWED_STREAM_SCHEMES, ALLOW_LOCAL_SOURCES

class InvalidSourceError(ValueError):
     """Exception raised when a source URL is invalid or not allowed."""

def validate_source(url:str):
        if not url or not isinstance(url, str):
            raise InvalidSourceError("URL must be a non-empty string.")

        url = url.strip()

        if not url.startswith(ALLOWED_STREAM_SCHEMES):
            raise InvalidSourceError(f"URL must start with one of the following schemes: {ALLOWED_STREAM_SCHEMES}")

        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            raise InvalidSourceError("URL must have a valid hostname.")

        if not ALLOW_LOCAL_SOURCES:
            try:
                ip = ipaddress.ip_address(socket.gethostbyname(host))

            except (socket.gaierror, ValueError):
                raise InvalidSourceError(f"Unable to resolve hostname: {host}")

            if (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_unspecified or ip.is_link_local):
                raise InvalidSourceError(f"Refusing to connect to non-public IP address: {ip}")

        return url
        

        
        