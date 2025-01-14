import re
from typing import Optional, Self
from collections.abc import Callable, Mapping

from pydantic import ConstrainedStr, HttpUrl
from semver import VersionInfo

from monkeytypes import (
    AgentPluginType,
    InfectionMonkeyBaseModel,
    InfectionMonkeyModelConfig,
    OperatingSystem,
)


class PluginName(ConstrainedStr):
    """
    A plugin name

    Allowed characters are alphanumerics and underscore.
    """

    strip_whitespace = True
    regex = re.compile("^[a-zA-Z0-9_]+$")


class PluginVersion(VersionInfo):
    @classmethod
    def __get_validators__(cls):
        """Return a list of validator methods for pydantic models."""
        yield cls.from_str

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Inject/mutate the pydantic field schema in-place."""
        field_schema.update(
            examples=[
                "1.0.2",
                "2.15.3-alpha",
                "21.3.15-beta+12345",
            ]
        )

    @classmethod
    def from_str(cls, version: str) -> Self:
        """Convert a string to a PluginVersion."""
        return cls.parse(version)


class AgentPluginManifest(InfectionMonkeyBaseModel):
    """
    Class describing agent plugin

    Attributes:
        :param name: Plugin name in snake case
        :param plugin_type: Type of the plugin (exploiter, fingerprinter,
         credentials collector, etc.)
        :param supported_operating_systems: Operating systems that the plugin can run on
        :param target_operating_systems: Operating systems that the plugin can target
        :param title: Human readable name for the plugin
        :param description: Description of the plugin
        :param version: Version of the plugin
        :param link_to_documentation: Link to the documentation of the plugin
        :param safe: Is the plugin safe to run. If there's a chance that running the plugin could
         disrupt the regular activities of the servers or the network, then the plugin is not safe.
    """

    name: PluginName
    plugin_type: AgentPluginType
    supported_operating_systems: tuple[OperatingSystem, ...] = (
        OperatingSystem.WINDOWS,
        OperatingSystem.LINUX,
    )
    target_operating_systems: tuple[OperatingSystem, ...] = (
        OperatingSystem.WINDOWS,
        OperatingSystem.LINUX,
    )
    title: Optional[str]
    version: PluginVersion
    description: Optional[str]
    remediation_suggestion: Optional[str] = None
    link_to_documentation: Optional[HttpUrl] = None
    safe: bool = False

    class Config(InfectionMonkeyModelConfig):
        json_encoders: Mapping[type, Callable] = {PluginVersion: lambda v: str(v)}
