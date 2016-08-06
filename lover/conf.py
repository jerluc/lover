# -*- coding: utf-8 -*-
import getpass
import os
import os.path

import yaml
from lover.platforms import get_current_platform


LATEST_LOVE_VERSION = '0.10.1'


class Configuration(object):
    def __init__(self, raw):
        self.raw = raw
        self.love_version = raw['loveVersion']
        self.identifier = raw['id']
        self.author = raw['author']
        self.name = raw['name']
        self.description = raw['description']
        self.targets = raw['targets']

    def as_dict(self):
        return self.raw.copy()


class MissingConfigurationException(Exception):
    def __init__(self):
        msg = 'No lover configuration found. Please recreate your '\
                'lover project with \'lover init\''
        Exception.__init__(self, msg)


class ExistingConfigurationException(Exception):
    def __init__(self):
        msg = 'Lover configuration file already exists. Did you mean' \
            ' to use \'lover new\'?'
        Exception.__init__(self, msg)


def get_input(prompt, default=None):
    if not default is None:
        prompt = '%s (default is \'%s\')' % (prompt, default)
    prompt = prompt + ': '
    while True:
        value = raw_input(prompt).strip()
        if not value:
            if default is None:
                print('Please enter a value')
            else:
                return default
        else:
            return value


def create_config(project_dir, config_file):
    identifier = get_input('Project idenitifer', default=project_dir)
    name = get_input('Project name', default=project_dir)
    desc = get_input('Project description', default='')
    author = get_input('Your name', default=getpass.getuser())
    love_version = get_input('LOVE version to use',
            default=LATEST_LOVE_VERSION)

    new_config = Configuration({
        'id': identifier,
        'name': name,
        'description': desc,
        'author': author,
        'loveVersion': love_version,
        'targets': [get_current_platform()]
    })

    with open(config_file, 'w') as f:
        f.write(yaml.dump(new_config.as_dict(), default_flow_style=False))


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = Configuration(yaml.load(f.read()))
        # TODO: Verify the contents of the config?
        return config


def get(directory, create=False):
    config_file = os.path.join(directory, '.lover.yaml')
    if not os.path.exists(config_file):
        if create:
            create_config(os.path.basename(directory), config_file)
        else:
            raise MissingConfigurationException()
    elif create:
        # If the configuration file already exists and we're trying to
        # create a new config, fail loadly
        raise ExistingConfigurationException()
    return load_config(config_file)

