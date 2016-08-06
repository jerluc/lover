# -*- coding: utf-8 -*-
import glob
import os.path
import plistlib
import shutil
import stat
import tempfile

import requests
from pyunpack import Archive

import lover.platforms as platforms


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
        extract(platform, env.download_file(platform=platform))
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


# TODO: Move this into platforms?
def post_extract(extracted_dir, platform):
    if platform in (platforms.WIN32, platforms.WIN64):
        extra_dir = glob.glob(os.path.join(extracted_dir,
            'love-*-win*'))[0]
        copytree(extra_dir, extracted_dir)
        shutil.rmtree(extra_dir)


def extract(platform, local_file):
    # Extract the downloaded local file into the same directory
    extracted_dir = os.path.dirname(local_file)
    Archive(local_file).extractall(extracted_dir)

    # TODO: Move this into platforms?
    post_extract(extracted_dir, platform)

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


# TODO: Put these ignores somewhere else?
def ignored_files(dir, files):
    dirname = os.path.basename(dir)
    if dirname.startswith('.') or dirname == 'dist':
        return files
    else:
        return []


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
    print('Archiving LOVE project \'%s\' into %s...' %
            (env.conf.identifier, os.path.relpath(env.love_file)))
    # Archives the project directory into a .love file
    if not os.path.exists(env.dist_dir):
        os.makedirs(env.dist_dir)

    # Creates the .zip file
    tmp_dir = tempfile.mkdtemp()
    copytree(env.project_dir, tmp_dir, ignore=ignored_files)
    shutil.make_archive(env.love_file, 'zip', tmp_dir)
    shutil.rmtree(tmp_dir)

    # Renames to .love, since shutil.make_archive() adds .zip
    os.rename(env.love_file + '.zip', env.love_file)
    print('Archival complete!')


def package(env, platform):
    print('Packaging LOVE project \'%s\' for platform \'%s\'...' %
            (env.conf.identifier, platform))

    love_dir = env.love_dir(platform=platform)
    output_dir = env.output_dir(platform=platform)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # TODO: Move this platform-specific behavior into platforms?
    if platform == platforms.MACOS:
        # Get the original love.app file
        love_app = os.path.join(love_dir, 'love.app')

        # Copy the love.app file into the output directory with project name
        output_app = os.path.join(output_dir, env.conf.identifier + '.app')
        shutil.copytree(love_app, output_app)

        # Copy the archived .love file into the new .app
        res = os.path.join(output_app, 'Contents', 'Resources')
        shutil.copy(env.love_file, res)

        # Modify the Info.plist file per the LOVE wiki instructions
        # https://love2d.org/wiki/Game_Distribution
        plist_file = os.path.join(output_app, 'Contents', 'Info.plist')
        plist = plistlib.readPlist(plist_file)
        plist['CFBundleIdentifier'] = env.conf.identifier
        del plist['UTExportedTypeDeclarations']
        plistlib.writePlist(plist, plist_file)
    if platform in (platforms.WIN32, platforms.WIN64):
        # Copy the original love directory contents
        copied_dir = os.path.join(output_dir, env.conf.identifier)
        # This should ignore the original download .zip file
        ignore = shutil.ignore_patterns('love*.zip')
        shutil.copytree(love_dir, copied_dir, ignore=ignore)

        # Concatenate .love file to the end of our love.exe copy
        love_exe = os.path.join(copied_dir, 'love.exe')
        with open(love_exe, 'ab') as f:
            with open(env.love_file) as love_file:
                f.write(love_file.read())

        # Rename the love.exe copy to {IDENTIFIER}.exe
        app_exe = os.path.join(copied_dir, '%s.exe' %
            env.conf.identifier)
        os.rename(love_exe, app_exe)

        # Create .zip file from the copied directory and clean up
        distro = os.path.join(output_dir, env.conf.identifier)
        shutil.make_archive(distro, 'zip', copied_dir)
        shutil.rmtree(copied_dir)


    print('Packaging complete!')

