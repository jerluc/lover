# -*- coding: utf-8 -*-
import os
import os.path
import sys
import platform


WIN32 = 'win-32bit'
WIN64 = 'win-64bit'
MACOS = 'darwin-64bit'
LINUX32 = 'linux-32bit'
LINUX64 = 'linux-64bit'

PLATFORM_DOWNLOAD_PATH = {
    WIN32: 'love-%(love_version)s-win32.zip',
    WIN64: 'love-%(love_version)s-win64.zip',
    MACOS: 'love-%(love_version)s-macosx-x64.zip',
    LINUX32: 'love_%(love_version)sppa1_i386.deb',
    LINUX64: 'love_%(love_version)sppa1_amd64.deb'
}

PLATFORM_EXECUTABLES = {
    WIN32: ('love.exe',),
    WIN64: ('love.exe',),
    MACOS: ('love.app', 'Contents', 'MacOS', 'love'),
    LINUX32: ('love'),
    LINUX64: ('love')
}


def executable(platform, love_version):
    return os.path.join(*PLATFORM_EXECUTABLES[platform]) % dict(
        love_version=love_version
    )


def get_current_platform():
    system = platform.system().lower()
    bits, _ = platform.architecture()
    return '%s-%s' % (system, bits)

