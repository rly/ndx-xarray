# Changelog for ndx-xarray

## 0.1.1 (2025-05-05)

### Changed
- Replaced usage of the deprecated `call_docval_func` from HDMF 4.0.
- Updated the extension to use the latest version of the `ndx-template` package, including using `pyproject.toml`.
- Reformatted the code to comply with the latest version of `black` and `ruff`.
- Added `scipy` as an explicit dependency in `pyproject.toml` to enable reading of netCDF files.
