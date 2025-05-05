# Changelog for ndx-xarray

## 0.1.2 (2025-05-05)

### Added
- Added README that was accidentally removed in the last release.

## 0.1.1 (2025-05-05)

### Changed
- Replaced usage of the deprecated `call_docval_func` from HDMF 4.0.
- Updated the extension to use the latest version of the `ndx-template` package, including using `pyproject.toml`.
- Reformatted the code to comply with the latest version of `black` and `ruff`.
- Added `scipy` as an explicit dependency in `pyproject.toml` to enable reading of netCDF files. This was used
  previously because `hdmf<4.0` listed `scipy` as a dependency, but it is no longer listed in the latest version of
  HDMF. Users can opt to use the netCDF4-python library instead.
