# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-xarray""",
        version="""0.1.1""",
        doc="""NWB extension to add support for storing/referencing external xarray files""",
        author=[
            "Ryan Ly",
        ],
        contact=[
            "rly@lbl.gov",
        ],
    )
    ns_builder.include_namespace("core")

    external_xarray_dataset = NWBGroupSpec(
        neurodata_type_def='ExternalXarrayDataset',
        neurodata_type_inc='NWBDataInterface',
        doc=('An NWB container that contains a reference to an xarray dataset stored in an external netCDF .nc file. '
             'The file should be stored in the netCDF4 format (the default when using Dataset.to_netcdf(...) on '
             'xarray >= v0.19.0, <= 1 with the netCDF4-python library available.'),
        attributes=[
            NWBAttributeSpec(
                name='description',
                doc='Description of the xarray dataset.',
                dtype='text'
            ),
            NWBAttributeSpec(
                name='path',
                doc='Relative file path to the xarray dataset.',
                dtype='text'
            )
        ],
    )

    new_data_types = [external_xarray_dataset]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
