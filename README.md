# ndx-xarray Extension for NWB

## Installation


## Usage
The `ExternalXarrayDataset` supports storage of paths to xarray datasets stored in netCDF-format files
with the suffix `.nc`. Files should be openable using `xr.open_dataset(path)`.

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
