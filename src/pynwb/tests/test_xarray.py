import datetime
import numpy as np
from pathlib import Path
import xarray as xr

from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file

from ndx_xarray import ExternalXarrayDataset


def set_up_nwbfile():
    """Create a basic NWB file for testing."""
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    return nwbfile


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


class TestExternalXarrayDataset(TestCase):

    def setUp(self):
        self.xr_path = "test_xarray.nc"
        write_xarray_dataset(self.xr_path)

    def tearDown(self):
        remove_test_file(self.xr_path)

    def test_constructor(self):
        """Test that the constructor for ExternalXarrayDataset sets values as expected."""
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=self.xr_path)

        self.assertEqual(xr_dset.name, "test_xarray")
        self.assertEqual(xr_dset.description, "desc")
        self.assertEqual(xr_dset.path, self.xr_path)

    def test_constructor_path(self):
        """Test that the constructor for ExternalXarrayDataset accepts and converts a pathlib.Path object."""
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=Path(self.xr_path))

        self.assertEqual(xr_dset.path, self.xr_path)

    def test_constructor_warn_wrong_ext(self):
        """Test that the constructor raises a warning when the path does not have suffix .nc."""
        msg = "ExternalXarrayDataset path should have extension .nc: wrong_extension"
        with self.assertWarnsWith(UserWarning, msg):
            ExternalXarrayDataset(name="test_xarray", description="desc", path="wrong_extension")

    def test_set_path_exists(self):
        """Test that setting the path after it has already been set fails."""
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=Path(self.xr_path))

        msg = "Cannot reset path."
        with self.assertRaisesWith(ValueError, msg):
            xr_dset.path = "test"

        self.assertEqual(xr_dset.path, self.xr_path)

    def test_add_scratch(self):
        """Test that an ExternalXarrayDataset can be added and retrieved from an NWB file's scratch space."""
        nwbfile = set_up_nwbfile()
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=self.xr_path)
        nwbfile.add_scratch(xr_dset)

        ret = nwbfile.get_scratch("test_xarray")
        self.assertIs(ret, xr_dset)

    def test_as_xarray(self):
        """Test getting an xarray.Dataset from an ExternalXarrayDataset."""
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=self.xr_path)
        xr_dset_object = xr_dset.as_xarray()
        self.assertTrue(isinstance(xr_dset_object, xr.Dataset))


class TestExternalXarrayDatasetRoundtrip(TestCase):
    """Simple roundtrip test for ExternalXarrayDataset."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"
        self.xr_path = "test_xarray.nc"
        write_xarray_dataset(self.xr_path)

    def tearDown(self):
        remove_test_file(self.path)
        remove_test_file(self.xr_path)

    def test_roundtrip(self):
        """
        Add a ExternalXarrayDataset to an NWBFile, write it to file, read the file, and test that the
        ExternalXarrayDataset from the file matches the original ExternalXarrayDataset.
        """
        xr_dset = ExternalXarrayDataset(name="test_xarray", description="desc", path=self.xr_path)
        self.nwbfile.add_scratch(xr_dset)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            ret = read_nwbfile.get_scratch("test_xarray")
            self.assertContainerEqual(ret, xr_dset)
