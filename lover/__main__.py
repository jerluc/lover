# -*- coding: utf-8 -*-
import os.path
import sys

import click

import lover
from lover.env import Env
import lover.commands as commands

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.path.abspath(os.getcwd())


@click.group(chain=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(version=lover.version, prog_name='lover')
def cli():
    pass


@cli.command('new')
@click.argument('project_dir', default=CWD)
@click.option('-r', '--recreate', is_flag=True,
              help='Recreates lover metafiles and LOVE binaries')
def new(project_dir, recreate):
    """Creates a new LOVE project"""
    env = Env(project_dir, autocreate=True)
    sys.exit(commands.new(env, recreate))


@cli.command('run')
def run():
    """Runs the current LOVE project"""
    env = Env(CWD)
    sys.exit(commands.run(env))


@cli.command('dist')
@click.option('-t', '--target', multiple=True, type=str,
              help='Specifies an output target for the distro')
def dist(target):
    """Creates a distributable binary"""
    env = Env(CWD)
    sys.exit(commands.dist(env, target))


def main():
    cli()
