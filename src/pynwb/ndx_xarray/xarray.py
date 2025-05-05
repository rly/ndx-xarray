from hdmf.utils import docval, get_docval, popargs
from pathlib import Path
from pynwb import register_class
from pynwb.base import NWBDataInterface
from warnings import warn
import xarray as xr


@register_class("ExternalXarrayDataset", "ndx-xarray")
class ExternalXarrayDataset(NWBDataInterface):

    __nwbfields__ = (
        "description",
        "path",
    )

    @docval(
        *get_docval(NWBDataInterface.__init__),
        {
            "name": "description",
            "type": str,
            "doc": "Description of the xarray dataset.",
        },
        {
            "name": "path",
            "type": (str, Path),
            "doc": "The relative file path to the xarray dataset.",
        },
    )
    def __init__(self, **kwargs):
        description, path = popargs("description", "path", kwargs)
        super().__init__(**kwargs)
        self.description = description
        if isinstance(path, Path):
            path = str(path)
        self.path = path

    @property
    def path(self):
        return self.fields.get("path")

    @path.setter
    @docval(
        {
            "name": "value",
            "type": (str, Path),
            "doc": "The relative file path to the xarray dataset.",
        },
    )
    def path(self, **kwargs):
        """Set the path of this ExternalXarrayDataset. Warn if file suffix is not ".nc"."""
        # Override auto-generated path setter
        if self.path is not None:
            raise ValueError("Cannot reset path.")

        value = popargs("value", kwargs)
        if Path(value).suffix != ".nc":
            warn("ExternalXarrayDataset path should have extension .nc: %s" % str(value))

        self.fields["path"] = str(value)

    def as_xarray(self):
        """Return an opened xarray.Dataset at this object's path. This Dataset should be closed after use."""
        return xr.open_dataset(self.path)
