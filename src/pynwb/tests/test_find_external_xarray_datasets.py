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


def get_container_hierarchy(container):
    """Return a list of the container hierarchy of the given container in reverse order (the root will be last).

    For example, given container A, return [A, A.parent, A.parent.parent, ..., root]
    """
    if container.parent is None:
        return [container]
    hierarchy = get_container_hierarchy(container.parent)
    hierarchy.insert(0, container)
    return hierarchy


def hierarchy_to_str(hierarchy):
    """Return a string with the type and name of each container in a container hierarchy, separated by commas."""
    ret = []
    for obj in hierarchy:
        ret.append("%s '%s'" % (type(obj), obj.name))
    return ", ".join(ret)


def test_find_external_xarray_datasets():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )

    path = "test.nwb"
    xr_path = "test_xarray2.nc"
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

    # find all ExternalXarrayDataset objects in the file.
    # this read block works regardless of whether "import ndx_xarray" was called earlier
    # in the python execution
    with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
        # if the extension python module has been imported, this line will return the custom API
        # class defined in the extension (ndx_array.xarray.ExternalArrayDataset).
        # otherwise, this line will return the class generated for reading data with this
        # neurodata type based on the cached namespace in the file (abc.ExternalArrayDataset).
        cls = io.manager.type_map.get_dt_container_cls("ExternalXarrayDataset", "ndx-xarray")

        read_nwbfile = io.read()
        count = 0
        print("All ExternalXarrayDataset objects found in the file:")
        for object_id, obj in read_nwbfile.objects.items():
            if isinstance(obj, cls):
                count += 1
                builder = io.manager.get_builder(obj)
                pynwb_hierarchy = hierarchy_to_str(get_container_hierarchy(obj))

                print("%d: %s '%s'" % (count, type(obj), obj.name))
                print("\tObject ID: %s" % object_id)
                print("\tHDF5 path: %s" % builder.path)
                print("\tPyNWB hierarchy: %s" % pynwb_hierarchy)
