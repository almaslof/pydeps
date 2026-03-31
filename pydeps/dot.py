# -*- coding: utf-8 -*-
"""
Graphviz interface.
"""
import os
import platform
import sys
from subprocess import Popen
import subprocess
import shlex

from . import cli

win32 = sys.platform == 'win32'


def is_unicode(s):  # pragma: nocover
    """Test unicode with py3 support.
    """
    try:
        return isinstance(s, unicode)
    except NameError:
        return False


def to_bytes(s):  # pragma: nocover
    """Convert an item into bytes.
    """
    if isinstance(s, bytes):
        return s
    if isinstance(s, str) or is_unicode(s):
        return s.encode("utf-8")
    try:
        return unicode(s).encode("utf-8")
    except NameError:
        return str(s).encode("utf-8")


def cmd2args(cmd):
    """Prepare a command line for execution by Popen.
    """
    if isinstance(cmd, str):
        return cmd if win32 else shlex.split(cmd)
    return cmd


DOT_TIMEOUT = 10


def pipe(cmd, txt, timeout=None):
    """Pipe `txt` into the command `cmd` and return the output.
       Returns None if the process is killed due to timeout.
    """
    proc = Popen(
        cmd2args(cmd),
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=win32
    )
    try:
        out, _ = proc.communicate(txt, timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return None
    return out


def _build_graphviz_cmd(engine, fmt, **kw):
    cmd = "%s -Gstart=1 -T%s" % (engine, fmt)
    for k, v in list(kw.items()):
        if v is True:
            cmd += " -%s" % k
        else:
            cmd += " -%s=%s" % (k, v)
    return cmd


def dot(src, **kw):
    """Execute the dot command to create an svg output.
    """
    fmt = kw.pop('T', 'svg')
    cmd = _build_graphviz_cmd('dot', fmt, **kw)
    return pipe(cmd, to_bytes(src))


def call_graphviz_dot(src, fmt):
    """Call dot command, and provide helpful error message if we
       cannot find it. Falls back to sfdp if dot takes longer than
       DOT_TIMEOUT seconds.
    """
    try:
        cmd = _build_graphviz_cmd('dot', fmt)
        print("Running: %s" % cmd, file=sys.stderr)
        svg = pipe(cmd, to_bytes(src), timeout=DOT_TIMEOUT)
    except OSError as e:  # pragma: nocover
        if e.errno == 2:
            cli.error("""
               cannot find 'dot'

               pydeps calls dot (from graphviz) to create svg diagrams,
               please make sure that the dot executable is available
               on your path.
            """)
        raise

    if svg is None:
        cmd = _build_graphviz_cmd('sfdp', fmt, Goverlap='false')
        print("dot timed out after %ds, falling back to: %s" % (DOT_TIMEOUT, cmd),
              file=sys.stderr)
        svg = pipe(cmd, to_bytes(src))
        if svg is None:
            raise RuntimeError("sfdp also failed to render the graph")

    return svg


def in_wsl():
    """Are we running under wsl?
    """
    return 'microsoft-standard' in platform.uname().release


def display_svg(kw, fname):  # pragma: nocover
    """Try to display the svg file on this platform.

       Note that this is also used to display PNG files, despite the name.
    """
    display = kw['display']
    if not display:
        display = os.getenv('PYDEPS_DISPLAY', os.getenv('BROWSER', None))

    if not display:
        cli.verbose("Displaying:", fname)
        if sys.platform == 'win32':
            os.startfile(fname)
        else:
            if sys.platform == "darwin":
                display = "open"
            elif in_wsl():
                # this is still borked...
                display = "/usr/bin/wslview"
            else:
                display = "xdg-open"
            subprocess.check_call([display, fname])
    else:
        cli.verbose(display + " " + fname)
        subprocess.check_call([display, fname])
