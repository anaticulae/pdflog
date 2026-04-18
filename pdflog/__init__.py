#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

from pdflog.info import generator
from pdflog.pages import determine as pagecount
from pdflog.version import parse as pdfversion

__version__ = importlib.metadata.version('pdflog')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'pdflog'

INVALID_PDF = 4
