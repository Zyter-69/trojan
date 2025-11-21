import keylogger as ky

x = input ("enter 1 to start keylogger \n enter 2 to stop keylogger")


if x == '1':
    ky.startKeylogger()

x = input ("enter 1 to start keylogger \n enter 2 to stop keylogger")
if x == '2':
    ky.stopKeylogger() 