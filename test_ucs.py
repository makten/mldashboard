from ucsmsdk.ucshandle import UcsHandle

# Connection
handle = UcsHandle("192.168.202.131", "ucspe", "ucspe")

#Login
handle.login()

print(handle.cookie)