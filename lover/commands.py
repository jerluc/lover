# -*- coding: utf-8 -*-
import functools
import os
import os.path
import multiprocessing
import subprocess
import sys

import lover.love as love


def new(env, recreate):
    if recreate:
        # TODO: Force-recreate project configs; not entirely sure if
        # this would even be useful...
        pass
    love.get(env)
    love.setup_project_dir(env)
    return 0


def run(env):
    love.get(env)
    love_proc = subprocess.Popen([env.love_binary(), env.project_dir])
    return love_proc.wait()


def dist(env, targets):
    targets = set(targets) | set(env.conf.targets)
    procs = multiprocessing.Pool(4)
    procs.map(functools.partial(love.get, env), targets)
    love.archive(env)
    # TODO: Do packaging here
    return 0

