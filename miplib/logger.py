from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = getLogger("warplex.miplib.logger")