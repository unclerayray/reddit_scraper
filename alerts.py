__doc__ = """Methods for audial and (possibly in the future) visual alerts."""

import subprocess

def alert(s):
    subprocess.call(["say", s])

speak = alert
say = alert
