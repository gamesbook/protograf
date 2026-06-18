__version_info__ = (0, 5, 4, "")
ver = ".".join(map(str, __version_info__))
__version__ = "".join(ver.rsplit(".", 1))  # remove last .
