import logging

from pysimavr.about import __version__


log = logging.getLogger(__name__)

log.debug('version=%s', __version__)
