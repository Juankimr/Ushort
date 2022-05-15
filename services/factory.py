import base64
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app import app


@dataclass
class Shortener(ABC):
    url: str = ''
    base_url: str = ''
    slug: str = ''

    @abstractmethod
    def _encode_slug(self):
        pass

    def shorten(self):
        self.slug = self._encode_slug()
        return f"{self.base_url}v1/{self.slug}"

    @abstractmethod
    def _decode_slug(self):
        pass

    def enlarge(self):
        return self._decode_slug()


class Base64Shortener(Shortener):

    def _encode_slug(self):
        message_bytes = self.url.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        url_encoded = base64_bytes.decode('ascii')
        return url_encoded

    def _decode_slug(self):
        base64_bytes = self.slug.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        url_decoded = message_bytes.decode('ascii')
        return url_decoded


class CustomShortener(Shortener):
    """
        Custom shortener
        Generate hash slug with adler32 encrypt
        and save it to redis.
        as key value
    """

    def _encode_slug(self):
        url_bytes = str.encode(self.url)
        slug = zlib.adler32(url_bytes)
        app.state.redis_service.set(key=slug, value=self.url)
        return slug

    def _decode_slug(self):
        url_decoded = app.state.redis_service.get(key=self.slug)
        return url_decoded
