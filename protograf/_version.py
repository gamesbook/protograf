__version_info__ = (0, 4, 5, "")
ver = ".".join(map(str, __version_info__))
__version__ = "".join(ver.rsplit(".", 1))  # remove last .
