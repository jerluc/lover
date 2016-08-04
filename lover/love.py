# -*- coding: utf-8 -*-
import os.path
import shutil
import stat
import tempfile

import requests
from pyunpack import Archive


# Templates for conf.lua and main.lua files
CONF_LUA = '''function love.conf(t)
    -- Package settings
    t.identity = "%(id)s"
    t.title = "%(title)s"
    t.version = "%(love_version)s"

    -- Window/display settings
    t.window.width = 800
    t.window.height = 600
    t.window.fullscreen = false
    t.window.fullscreentype = "desktop"
    t.window.highdpi = false

    -- More LOVE configuration options go here
end
'''

MAIN_LUA = '''function love.draw()
    love.graphics.print("Hello World", 400, 300)
end
'''


def get(env, platform=None):
    if not platform:
        platform = env.platform
    # Only try to download/extract if it doesn't already exist
    if not os.path.exists(env.love_binary(platform=platform)):
        # Only try to download if the .zip doesn't already exist
        if not os.path.exists(env.download_file(platform=platform)):
            print('Downloading LOVE (%s; %s)...' %
                    (env.conf.love_version, platform))
            download(env.download_url(platform=platform),
                    env.download_file(platform=platform))
            print('Download complete!')
        print('Extracting LOVE (%s; %s)...' % (env.conf.love_version,
            platform))
        extract(env.download_file(platform=platform))
        st = os.stat(env.love_binary(platform=platform))
        os.chmod(env.love_binary(platform=platform),
                st.st_mode | stat.S_IEXEC)
        print('Extraction complete!')


def download(download_url, local_file):
    local_dir = os.path.dirname(local_file)
    # Create the parent directories if needed
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Actually do the file download
    r = requests.get(download_url)
    with open(local_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def extract(local_file):
    # Extract the downloaded local file into the same directory
    extracted_dir = os.path.dirname(local_file)
    Archive(local_file).extractall(extracted_dir)


def setup_project_dir(env):
    # Creates conf.lua and main.lua files for the new project
    conf_lua_file = os.path.join(env.project_dir, 'conf.lua')
    main_lua_file = os.path.join(env.project_dir, 'main.lua')

    if not os.path.exists(conf_lua_file):
        with open(conf_lua_file, 'wb') as f:
            contents = CONF_LUA % dict(
                    id = env.conf.identifier,
                    title = env.conf.name,
                    love_version = env.conf.love_version
            )
            f.write(contents)

    if not os.path.exists(main_lua_file):
        with open(main_lua_file, 'wb') as f:
            f.write(MAIN_LUA)


def copytree(src, dst, symlinks=False, ignore=None):
    '''
    A really shitty work-around for the fact that shutil.copytree()
    requires the destination directory to not exist (which makes it hard
    when I try to use a temporary directory!).

    http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
    '''
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def archive(env):
    love_file = os.path.join(env.dist_dir, env.conf.identifier)
    print('Archiving LOVE project \'%s\' into %s.love...' %
            (env.conf.identifier, os.path.relpath(love_file)))
    # Archives the project directory into a .love file
    if not os.path.exists(env.dist_dir):
        os.makedirs(env.dist_dir)

    # Creates the .zip file
    # TODO: Put these ignores somewhere else?
    ignore = shutil.ignore_patterns('^.git', '.svn', '.DS_Store')
    tmp_dir = tempfile.mkdtemp()
    copytree(env.project_dir, tmp_dir, ignore=ignore)
    shutil.make_archive(love_file, 'zip', tmp_dir)
    shutil.rmtree(tmp_dir)

    # Renames to .love
    os.rename(love_file + '.zip', love_file + '.love')
    print('Archival complete!')

