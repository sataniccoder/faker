import os, time

"""
This is a test/example modules

you can use this as a template to create your own module's

NEEDED FUNCTIONS
info
start
stop


this is a template module
"""
# step 1/4
# this is used to help stop the program

# use this function to preform a clean shutdown of the module
def stop():
    if "test.txt" in os.listdir():
        os.remove("test.txt")

# step 2/4

def info():
    return "port:int,name:str"

# step 3/4

# this is where the program excutes it's code
# put anything you want here
# since this is a simple test, all it does is create a file, wait 3 seconds, deletes it and so on

# WARNING: "stop_event" has to be here or it won't shutdown
def start(stop_event,port,name):
    data = str("YO IT WORKS -> "+str(port)+name)

    run = True
    while run:
        time.sleep(3)
        file = open("test.txt", "x+")
        file.write(data)
        file.close()

        time.sleep(3)
        os.remove("test.txt")

        # at the end of each program 'loop' check for the stop_event
        if stop_event.is_set():
            stop()
            run = False


# step 4/4


# install is the function called when you try to install a module
# from the program, here you will have any code you need to run as-well 
# as any commands needed to run for the install (EG "pip install flask")
def install():
    print("installing test module V0.1")
    print("this is a simple module to test and make sure you have everything setup properly")
    print("installing packages (0/4)")