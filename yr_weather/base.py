import requests
from requests_cache import CachedSession


class BaseClient:
    def __init__(self, headers: dict, use_cache: bool = True) -> None:
        if not isinstance(headers, dict):
            raise TypeError("The 'headers' parameter must be of type 'dict'.")

        self._baseURL = "https://api.met.no/weatherapi/"
        self._global_headers = headers

        if use_cache:
            self.session = CachedSession(cache_name="yr_cache", cache_control=True)
        else:
            self.session = requests.Session()

        self.session.headers = self._global_headers

    def set_headers(self, headers: dict) -> dict:
        """Set new headers of the client.

        This will override any old headers, and replace them with the new headers from the ``headers`` parameter.

        Parameters
        ----------
        headers: :class:`dict`
            The new headers, which will override the old ones.

        Returns
        -------
        :class:`dict`
            The headers which were set.
        """
        if not isinstance(headers, dict):
            raise TypeError("The 'headers' parameter must be of type 'dict'.")

        self._global_headers = headers
        self.session.headers = headers
        return self.session.headers

    def toggle_cache(self, toggle: bool) -> bool:
        """Toggle the usage of cache on or off.

        Parameters
        ----------
        toggle: :class:`bool`
            Whether cache should be used, or whether to disable it.

        Returns
        -------
        :class:`bool`
            The new state of the cache (on/off).
        """
        if toggle:
            if not isinstance(self.session, CachedSession):
                self.session = CachedSession(cache_name="yr_cache", cache_control=True)
                self.session.headers = self._global_headers
            return True
        else:
            if not isinstance(self.session, requests.Session):
                self.session = requests.Session()
                self.session.headers = self._global_headers
            return False
