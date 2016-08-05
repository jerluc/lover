# -*- coding: utf-8 -*-
import os.path

import lover.conf as conf
import lover.platforms as platforms


DOWNLOAD_TEMPLATE = 'https://bitbucket.org/rude/love/downloads/%s'
# TODO: Put this into the lover.platforms package when we need to add
# Linux support (as presently they are .deb files)
DOWNLOAD_FILE_TEMPLATE = 'love-%s-%s.zip'


class Env(object):
    def __init__(self, dir, autocreate=False):
        self.project_dir = dir
        if not os.path.exists(dir) and autocreate:
            os.makedirs(dir)
        self.platform = platforms.get_current_platform()
        self.conf = conf.get(dir, create=autocreate)

    def lover_dir(self):
        return os.path.join(os.path.expanduser('~'), '.lover')

    def love_dir(self, platform=None, love_version=None):
        if not platform:
            platform = self.platform
        if not love_version:
            love_version = self.conf.love_version
        return os.path.join(
            self.lover_dir(),
            love_version,
            platform
        )

    def love_binary(self, platform=None, love_version=None):
        if not platform:
            platform = self.platform
        if not love_version:
            love_version = self.conf.love_version
        executable = platforms.executable(platform, love_version)
        return os.path.join(
            self.love_dir(platform=platform, love_version=love_version),
            executable
        )

    def download_url(self, platform=None, love_version=None):
        if not platform:
            platform = self.platform
        if not love_version:
            love_version = self.conf.love_version
        download_platform = platforms.PLATFORM_DOWNLOAD_PATH[platform]
        download_file = DOWNLOAD_FILE_TEMPLATE % (love_version,
                download_platform)
        return DOWNLOAD_TEMPLATE % download_file

    def download_file(self, platform=None, love_version=None):
        if not platform:
            platform = self.platform
        if not love_version:
            love_version = self.conf.love_version
        download_platform = platforms.PLATFORM_DOWNLOAD_PATH[platform]
        download_file = DOWNLOAD_FILE_TEMPLATE % (love_version,
                download_platform)
        return os.path.join(
            self.love_dir(platform=platform, love_version=love_version),
            download_file
        )

    @property
    def dist_dir(self):
        return os.path.join(
            self.project_dir,
            'dist'
        )

    @property
    def love_file(self):
        return os.path.join(
            self.dist_dir,
            self.conf.identifier + '.love'
        )

    def output_dir(self, platform=None, love_version=None):
        if not platform:
            platform = self.platform
        if not love_version:
            love_version = self.conf.love_version
        return os.path.join(
            self.dist_dir,
            love_version,
            platform
        )

