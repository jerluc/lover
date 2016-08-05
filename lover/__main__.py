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


@cli.command('new', short_help='Creates a new LOVE project')
@click.argument('project_dir', default=CWD)
@click.option('-r', '--recreate', is_flag=True,
              help='Recreates lover metafiles and LOVE binaries')
def new(project_dir, recreate):
    """Creates a new LOVE project

    If PROJECT_DIR is provided, the new project will be created there.
    Otherwise, the new configuration and project files will be generated
    in the current directory."""
    env = Env(project_dir, autocreate=True)
    sys.exit(commands.new(env, recreate))


@cli.command('run', short_help='Runs your project')
def run():
    """Runs your project

    Loads the project configuration from the current directory and runs
    the project.

    If the LOVE version specified is not currently avaiable on your
    system, lover will automatically download the version specified in
    your project configuration before attempting to run."""
    env = Env(CWD)
    sys.exit(commands.run(env))


@cli.command('dist', short_help='Packages your project for distribution')
@click.option('-t', '--target', multiple=True, type=str, metavar='TARGET',
              help='Specifies an output target platform')
def dist(target):
    """Packages your project for distribution

    By default, this will load the project configuration from the
    current directory and create packaged distros for each target
    platform configured.

    To package additional targets that have not been preconfigured,
    specify multiple TARGETs during invocation.

    If any LOVE binary is not currently available for the configured
    target platforms, they will be automatically downloaded during this
    step before attempting to package."""
    env = Env(CWD)
    sys.exit(commands.dist(env, target))


def main():
    cli()
