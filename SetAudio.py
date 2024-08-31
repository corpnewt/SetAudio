import os, sys
from Scripts import *

class App:
    def __init__(self):
        self.r = run.Run()
        self.u = utils.Utils("Set Audio")
        script_name = self._get_script()
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scripts",script_name)
        self.a = applescript.Applescript()
        self.ins = None
        self.outs = None

    def _get_script(self):
        # Check if we're on macOS 13 or newer
        try:
            sw_vers = int(self.r.run({"args":["sw_vers","-productVersion"]})[0].strip().split(".")[0])
            if sw_vers >= 13:
                return "SetAudio13.txt"
        except:
            pass
        return "SetAudio.txt"

    def get_inputs_outputs(self):
        # Runs system_profiler SPAudioDataType and parses data
        n_head = "        " # Sets the pad for the name header
        n_foot = ":"        # Sets the last char for the header
        devs = self.r.run({"args":["system_profiler","-xml","SPAudioDataType"]})[0]
        dev_list = []
        try:
            xml = plist.loads(devs)
        except:
            xml = []
        if not len(xml):
            return []
        if not "_items" in xml[0] or not len(xml[0]["_items"]) or not "_items" in xml[0]["_items"][0]:
            return []
        audio_devices = xml[0]["_items"][0]["_items"]
        # Walk the list
        for x in audio_devices:
            try:
                new_item = {
                    "name": x.get("_name","Unknown"),
                    "out_source": x.get("coreaudio_output_source",None),
                    "out_count": x.get("coreaudio_device_output",None),
                    "in_source": x.get("coreaudio_input_source",None),
                    "in_count": x.get("coreaudio_device_input",None),
                    "type": x.get("coreaudio_device_transport",None)
                }
                dev_list.append(new_item)
            except:
                continue
        return dev_list
            
    def get_ins_outs(self):
        io = self.get_inputs_outputs()
        self.ins = []
        self.outs = []
        for x in io:
            if x["in_source"]:
                self.ins.append(x)
            if x["out_source"]:
                self.outs.append(x)
        # Sort the lists by their output types
        self.ins.sort(key=lambda x: x["type"])
        self.outs.sort(key=lambda x: x["type"])
        
    def parse_commands(self, comm):
        if not type(comm) is list:
            comm = [comm]
        if self.ins == None or self.outs == None:
            self.get_ins_outs()
        for x in comm:
            # Check for outputs first
            output = inputval = False
            if "o" in x.lower():
                x = x.lower().replace("o","")
                output = True
            elif "i" in x.lower():
                x = x.lower().replace("i","")
                inputval = True
            if not output and not inputval:
                continue
            # Try to get the index, and verify it
            try:
                ind = int(x)
            except:
                continue
            text = "output"
            if output:
                if ind > len(self.outs) or ind < 1:
                    continue
            else:
                text = "input"
                if ind > len(self.ins) or ind < 1:
                    continue
            # If type is airport - add 1 to the value to account for
            # the spacer
            with open(self.path, "r") as f:
                script = f.read()
            # Replace the values
            script = script.replace("[[inout]]",text).replace("[[row]]",str(ind))
            # Run the command
            out = self.a.run(script)
            if not out[2] == 0:
                print("Error!")
                print(out[1])

    def main(self):
        self.u.head()
        print("")
        self.get_ins_outs()
        print("Outputs:")
        print("")
        if not len(self.outs):
            print(" - None")
        else:
            for x,y in enumerate(self.outs,1):
                print(" - {}. {} - {}".format(x,y["name"],y["out_source"]))
        print("")
        print("Inputs:")
        print("")
        if not len(self.ins):
            print(" - None")
        else:
            for x,y in enumerate(self.ins,1):
                print(" - {}. {} - {}".format(x,y["name"],y["in_source"]))
        print("")
        print("Q. Quit")
        print("")
        menu = self.u.grab("Please select an input/output then value (i1, o3, etc):  ")
        if not len(menu):
            return
        if menu.lower() == "q":
            self.u.custom_quit()
        self.parse_commands(menu)

if __name__ == '__main__':
    # os.chdir(os.path.dirname(os.path.realpath(__file__)))
    a = App()
    if len(sys.argv) > 1:
        a.parse_commands(sys.argv[1:])
    else:
        while True:
            a.main()
