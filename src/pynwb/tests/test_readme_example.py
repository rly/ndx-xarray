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

xr_dset = ExternalXarrayDataset(name="test_xarray", path=xr_path)
nwbfile.add_scratch(xr_dset)

with NWBHDF5IO(path, mode="w") as io:
    io.write(nwbfile)

with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    ret = read_nwbfile.get_scratch("test_xarray")
    print(ret)
