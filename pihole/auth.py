from typing import Optional
from base64 import b64encode


class PiHoleAuth(object):
    """Wrapper for PiHole authentication data"""

    _web_passwd: str
    _http_auth: Optional[str]

    def __init__(self, web_passwd: str, http_auth: Optional[str] = None) -> None:
        """Build a PiHoleAuth object

        Args:
            web_passwd (str): Web password
            http_auth (Optional[str], optional): Optional HTTP basic auth payload. Defaults to None.
        """

        self._web_passwd = web_passwd
        self._http_auth = http_auth

    def set_http_credentials(self, username: str, password: str) -> None:
        """Enable HTTP basic auth

        Args:
            username (str): HTTP auth username
            password (str): HTTP auth password
        """

        self._http_auth = b64encode(f"{username}:{password}").decode()
