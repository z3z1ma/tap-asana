"""Custom client handling, including AsanaStream base class."""

from functools import lru_cache
from typing import Iterable, Optional

import asana
from singer_sdk.streams import Stream


class AsanaStream(Stream):
    """Stream class for Asana streams."""

    primary_keys = ["gid"]

    def __init__(self, resource_name: str, *args, **kwargs) -> None:
        self.resource_name = resource_name
        super().__init__(*args, **kwargs)

    @property
    @lru_cache
    def client(self) -> asana.Client:
        """Return a client object."""

        token = self.config.get("access_token")
        if not token:
            client = asana.Client.oauth(
                client_id=self.config["client_id"],
                client_secret=self.config["client_secret"],
                redirect_uri=self.config["redirect_uri"],
            )
        client = asana.Client.access_token(token)
        client.session.refresh_token(
            client.session.token_url,
            client_id=self.config.get("client_id"),
            client_secret=self.config.get("client_secret"),
            refresh_token=self.config.get("refresh_token"),
        )
        return client

    def _get_objects(self):
        yield from getattr(self.client, self.resource_name).find_all(
            page_size=self.config.get("page_size", 100)
        )

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        for record in self._get_objects():
            yield record
