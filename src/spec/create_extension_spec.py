# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec
# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension to add support for storing/referencing external xarray files""",
        name="""ndx-xarray""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_type('NWBDataInterface', namespace='core')

    external_xarray_dataset = NWBGroupSpec(
        neurodata_type_def='ExternalXarrayDataset',
        neurodata_type_inc='NWBDataInterface',
        doc=('An NWB container that contains a reference to an xarray dataset stored in an external netCDF file. '
             'The file should be stored in the netCDF4 format (the default when using Dataset.to_netcdf(...) on '
             'xarray v0.19.0 with the netCDF4-python library available. The netCDF4 format stores data is an '
             'HDF5 file with netCDF4 API features.'),
        attributes=[
            NWBAttributeSpec(
                name='path',
                doc='The relative file path to the xarray dataset.',
                dtype='text'
            )
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [external_xarray_dataset]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
