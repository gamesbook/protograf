__version_info__ = (0, 1, 0, "a44")
ver = ".".join(map(str, __version_info__))
__version__ = "".join(ver.rsplit(".", 1))  # remove last .
