import logging
import os

from . import mcp
from .core import live
from .tools import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    live.install_extension()
    live.start()
    mcp.run(transport='stdio')
    # The live bridge's connection threads are not daemons; without a hard exit an
    # ended Claude session leaves this process holding the port and the Aseprite link.
    os._exit(0)
