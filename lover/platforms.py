# -*- coding: utf-8 -*-
import os
import os.path
import sys
import platform


WIN32 = 'win-32bit'
WIN64 = 'win-64bit'
MACOS = 'darwin-64bit'

PLATFORM_DOWNLOAD_PATH = {
    WIN32: 'win32',
    WIN64: 'win64',
    MACOS: 'macosx-x64'
}

PLATFORM_EXECUTABLES = {
    WIN32: ('love-%(love_version)s-win32', 'love.exe'),
    WIN64: ('love-%(love_version)s-win64', 'love.exe'),
    MACOS: ('love.app', 'Contents', 'MacOS', 'love')
}


def executable(platform, love_version):
    return os.path.join(*PLATFORM_EXECUTABLES[platform]) % dict(
        love_version=love_version
    )


def get_current_platform():
    system = platform.system().lower()
    bits, _ = platform.architecture()
    return '%s-%s' % (system, bits)

