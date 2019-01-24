import sys, os
sys.path.append(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))
import run

class Applescript:

    def __init__(self):
        self.r = run.Run()
        return

    def run(self, command = None, sep = "\n"):
        # Reveals the passed path in Finder - only works on macOS
        if not sys.platform == "darwin":
            return ("", "macOS Only", 1)
        if not command:
            # No path sent - nothing to reveal
            return ("", "No command specified", 1)
        comm = ["osascript"]
        # Build our command, using one line at a time
        for x in command.split(sep):
            comm.extend(["-e",x])
        return self.r.run({"args" : comm})