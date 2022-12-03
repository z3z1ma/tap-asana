"""Asana tap class."""

from typing import List

from asana import resources
from singer_sdk import Stream, Tap

from tap_asana.streams import AsanaStream

# Exclude these resources from the catalog as
# they are not data sources we want to sync.
EXCLUDED_RESOURCES = [
    "gen",
    "audit_log_api",
    "batch_api",
    "custom_field_settings",
    "custom_fields",
    "organization_exports",
    "typeahead",
    "webhooks",
]


class TapAsana(Tap):
    """Asana tap class."""

    name = "tap-asana"

    config_jsonschema = {}

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return (
            AsanaStream(
                tap=self,
                resource_name=resource,
                name=resource,
                schema={
                    "properties": {"gid": {"type": "string"}},
                    "additionalProperties": True,
                },
            )
            for resource in resources.__dict__.keys()
            if not resource.startswith("_") and resource not in EXCLUDED_RESOURCES
        )


if __name__ == "__main__":
    TapAsana.cli()
