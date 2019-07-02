#!/usr/bin/env python
import os, sys
from Scripts import *

class App:
    def __init__(self):
        self.r = run.Run()
        self.u = utils.Utils("Font Rendering")

    def main(self):
        self.u.head()
        print("")
        out = self.r.run({"args":["defaults","read","-g","CGFontRenderingFontSmoothingDisabled"]})
        smooth = True
        if out[2]!=0 or out[0].strip()=="1":
            smooth = False
        print("Font Smoothing: {}".format("Enabled" if smooth else "Disabled"))
        print("")
        print("S. {} Font Smoothing".format("Disable" if smooth else "Enable"))
        print("Q. Quit")
        print("")
        menu = self.u.grab("Please select an option:  ")
        if not len(menu):
            return
        if menu.lower() == "q":
            self.u.custom_quit()
        elif menu.lower() == "s":
            self.u.head("{}abling Font Smoothing".format("Dis" if smooth else "En"))
            print("")
            if smooth:
                # Disable the setting
                print("defaults delete -g CGFontRenderingFontSmoothingDisabled")
                out = self.r.run({"args":["defaults","delete","-g","CGFontRenderingFontSmoothingDisabled"]})
            else:
                # Enable smoothing
                print("defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO")
                out = self.r.run({"args":["defaults","write","-g","CGFontRenderingFontSmoothingDisabled","-bool","NO"]})
            print("")
            if out[2]!=0:
                print("Something went wrong! :(")
            else:
                print("Done.  You must log out/restart for changes to take effect.")
            print("")
            self.u.grab("Press [enter] to return...")

if __name__ == '__main__':
    # os.chdir(os.path.dirname(os.path.realpath(__file__)))
    a = App()
    while True:
        a.main()