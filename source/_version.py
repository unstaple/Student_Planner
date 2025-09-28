# _version.py
try:
    from setuptools_scm import get_version
    VERSION = get_version(root='..', relative_to=__file__)
except Exception:
    # fallback
    VERSION = "0+unknown"
