#!/usr/bin/env python
# encoding: utf-8
"""
export.py

Export objects from a scout database

Created by Måns Magnusson on 2016-05-11.
Copyright (c) 2016 ScoutTeam__. All rights reserved.

"""

import logging

import click


LOG = logging.getLogger(__name__)

from .variant import variants, verified
from .hpo import hpo_genes
from .transcript import transcripts
from .gene import genes
from .panel import panel
from .case import cases
from .mitochondrial_report import mt_report


@click.group()
def export():
    """
    Export objects from the mongo database.
    """
    LOG.info("Running scout export")
    pass

export.add_command(panel) # done
export.add_command(genes) # done
export.add_command(transcripts) # done
export.add_command(variants) # done
export.add_command(verified) # done
export.add_command(hpo_genes) # done
export.add_command(cases) # done
export.add_command(mt_report)
