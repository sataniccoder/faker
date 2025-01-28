import os
import importlib
from threading import Thread
from threading import Event
import shutil

# local imports
from core.banner import bann

class mods:
    def __init__(self):
        self.mods = os.listdir("modules")
        
        self.active = {} # json of active modules
        
        self.module_data = [] # module var to be stored


        self.help = """

            -- CONTROL --        
list               : list all modules
use  <moduleID>    : select a module to use
stop <moduleID>    : select a running module to stop  
update             : (NOT DONE) update module load list (warning all currently active modules will be closed)
install <path/url> : (GITHUB NOT DONE) install a new module, either via a git url or a folder

            -- MISC --
exit               : exit the program
clear              : clear screen 
info               : display info on current modules
banner             : display the banner & info
        """


    # the start is where input is taken and passed off too 'handle_input'
    # the reason why i have done this is incase input sanitzeation is needed
    # as the project evolves
    def start(self):
        self.mods_info()

        print("rember type 'help' at any time for a list of commands")
        while True:
            inp = input("> ")
            self.handle_input(inp)


    def handle_input(self, inp):
        # misc
        if inp == "help":
            print(self.help)
        elif inp == "clear":
            os.system("clear")
        elif inp == "info":
            self.mods_info()
        elif inp == "exit":
            self.shutdown()
        elif inp == "banner":
            bann()
            self.mods_info()

        # control
        elif "use" in inp:
            self.load_module(inp)
        elif "stop" in inp:
            self.stop_module(inp)
        elif inp == "update":
            print("[ ! ] update function not done [ ! ]")
        elif "install" in inp:
            self.install_module(inp)

        # error
        else:
            print("[ ! ] unkown command [ ! ]")
            print("rember type 'help' at any time for a list of commands")


    # module handling
    def install_module(self, inp):
        inp = inp.split(" ")[1]


        # check if https
        if "https" in inp and "github" in inp:
            print("installing from github")
        else:
            if os.path.exists(inp) != True:
                print("[ ! ] please use the full module path (EG: /home/user/Downloads) [ ! ]")

            # means it's a dir
            mod_name = inp.split("/")[len(inp.split("/")) - 1]

            print("moving "+mod_name+" into modules")
            shutil.move(inp, "modules")
            print("installing...")

            mod_name = "modules."+mod_name+"."+mod_name
            installer = importlib.import_module(mod_name)
            install = getattr(installer, "install")
            install()

            print(mod_name.split(".")[len(mod_name.split("."))-1]+" installed")
            


    def stop_module(self, inp):
        inp = inp.split(" ")[1]
        if inp not in self.active:
            print("[ ! ] module "+inp+" isn't running [ ! ]")
        else:
            print("stopping "+inp)
            self.active[inp]["stop"].set()
            print("waiting for the module safly exit")
            self.active[inp]["thread"].join()

            del self.active[inp]

            print(inp + " safely stopped")


    
    def load_module(self, inp):
        # load modules
        inp = inp.split(" ")[1]
        print("loading "+inp)

        # check if modules exists
        if inp not in os.listdir("modules/"):
            print("[ ! ] could not fine module ("+inp+") [ ! ]")
        else:
            # load module
            mod = "modules."+inp+"."+inp
            module = importlib.import_module(mod)

            # grab needed start data
            info_func = getattr(module, "info")
            out = info_func()


            # create arguments
            data = {}

            # stop_event creation
            stop_event = Event()
            data["stop_event"] = stop_event
            
            for i in out.split(","):
                i = i.split(":")
                if i[1] == "int":
                    while True:
                        chk = input("[INPUT] "+i[0]+" INT > ")
                        try:
                            chk = int(chk)
                            data[i[0]] = chk
                            break
                        except ValueError:
                            print("[ ! ] needs to be a number [ ! ]")
                        
                elif i[1] == "str":
                    chk = input("[INPUT] "+i[0]+" STR > ")
                    data[i[0]] = chk
                
            # start the module 
            # this requirs some wiered shit tho
            start_func = getattr(module, "start")

            def create_threadable():
                # unpack data
                return start_func(**data)
            # TODO: add to POOL so it can run in background


            thr = Thread(target=create_threadable)
            thr.start()

            # wrap up
            print("module "+inp+" running")

            self.active[inp] = {"thread": thr, "stop": stop_event}

    # misc

    def shutdown(self):
        print("shutting down")
        print("removing pyache files...",end="")
        shutil.rmtree("core/__pycache__")
        for i in os.listdir("modules"):
            if "__pycache__" in os.listdir("modules/"+i):
                shutil.rmtree("modules/"+i+"/__pycache__")
        print(" [DONE]")

        print("Bye!")
        quit()

    def mods_info(self):
        info = """
Modules  : """+str(len(self.mods))+ """
Active   : """+str(len(self.active))+ """
Inactive : """+str(len(self.mods) - len(self.active))+"""

        """

        print(info)
