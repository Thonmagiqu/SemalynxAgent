from flask import Flask, request
from shared_memory_dict import SharedMemoryDict
import socket
import os
    
app = Flask(__name__)
smd=SharedMemoryDict("OS",1000)

@app.route("/ip", methods=["POST"])
def getIp():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
       
    return IPAddr

@app.route("/hostname", methods=["POST"])
def getHostname():
    hostname=socket.gethostname()   
    return hostname
    
@app.route("/reboot", methods=["POST"])
def remoteReboot():
    os.system("shutdown -r +1")
    return "Rebooting"

@app.route("/getos", methods=["POST"])
def getOS():
    return smd["os"]

if __name__ == "__main__":
    app.run(host="0.0.0.0")