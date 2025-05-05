# ndx-xarray Extension for NWB

The ndx-xarray NWB extension provides a standardized way for [xarray](https://docs.xarray.dev/en/stable/) datasets to be referenced in NWB files and opened using the `ndx_xarray` Python package.

## Installation

ndx-xarray is not yet installable through PyPI. In the meantime, you can use:
```
python -m pip install git+https://github.com/rly/ndx-xarray
```

## Design

Xarray datasets are typically very large (over 1 GB), contain more structured metadata than an HDF5 dataset, and is primarily opened using xarray. As such, it is best to store these datasets in a native xarray format outside of the NWB file, rather than as a specially formatted HDF5 dataset or other nonstandard form within an NWB file. We can then reference these external files from the NWB file by storing a relative path string from the NWB file to the external files.

The `ExternalXarrayDataset` data type extends `NWBDataInterface` and can therefore be added to the `acquisition` group and `scratch` group of an NWB file, and within `ProcessingModule` and other types in an NWB file.

The `ExternalXarrayDataset` data type has two required attributes:
- `description` - a description of the dataset
- `path` - the relative path from the NWB file to the external xarray file

## Python usage
The `ExternalXarrayDataset` supports storage of paths to xarray datasets stored in netCDF-format files
with the suffix `.nc`. Files should be openable using `xr.open_dataset(path)`.

The file should be stored in the netCDF4 format (the default when using `Dataset.to_netcdf(...)` on
`xarray >= v0.19.0` with the netCDF4-python library available.

`ExternalXarrayDataset` objects have a method `as_xarray()` which opens the xarray file as an xarray dataset.

```python
import datetime
import numpy as np
import xarray as xr

from pynwb import NWBHDF5IO, NWBFile

from ndx_xarray import ExternalXarrayDataset


def write_xarray_dataset(xr_path):
    """Write an xarray dataset to disk at the given path."""
    temp = 15 + 8 * np.random.randn(2, 2, 3)
    precip = 10 * np.random.rand(2, 2, 3)
    lon = [[-99.83, -99.32], [-99.79, -99.23]]
    lat = [[42.25, 42.21], [42.63, 42.59]]
    ds = xr.Dataset(
        {
            "temperature": (["x", "y", "time"], temp),
            "precipitation": (["x", "y", "time"], precip),
        },
        coords={
            "lon": (["x", "y"], lon),
            "lat": (["x", "y"], lat),
        },
    )
    ds.to_netcdf(xr_path)


nwbfile = NWBFile(
      session_description="session_description",
      identifier="identifier",
      session_start_time=datetime.datetime.now(datetime.timezone.utc)
)

path = "test.nwb"
xr_path = "test_xarray.nc"
write_xarray_dataset(xr_path)

# ExternalXarrayDataset requires a name, description, and relative path to an xarray file (.nc)
xr_dset1 = ExternalXarrayDataset(name="test_xarray1", description="test description", path=xr_path)

# ExternalXarrayDataset extends NWBDataInterface and so it can be added to the NWBFile's acquisition
# group, analysis group, scratch space, or a processing module
nwbfile.add_scratch(xr_dset1)

xr_dset2 = ExternalXarrayDataset(name="test_xarray2", description="test description", path=xr_path)
nwbfile.add_analysis(xr_dset2)

with NWBHDF5IO(path, mode="w") as io:
    io.write(nwbfile)

with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    ret_xr_dset1 = read_nwbfile.get_scratch("test_xarray1")
    print(ret_xr_dset1)
    print(ret_xr_dset1.as_xarray())

    ret_xr_dset2 = read_nwbfile.get_analysis("test_xarray2")
    print(ret_xr_dset2)
    print(ret_xr_dset2.as_xarray())
```


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).