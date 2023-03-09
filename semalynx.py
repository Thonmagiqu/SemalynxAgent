from flask import Flask, flash, request, render_template, redirect, url_for
import requests, json, operator


app = Flask(__name__) 
app.secret_key ="f3cfe9ed8fae309f02079dbf"


def loadsemaboxeslist():
    with open("semaboxes.json", "r") as f:
        liste_semabox=json.load(f)
        f.close()
    return liste_semabox

def deleteSemaboxFromList(name):
    liste_semabox=loadsemaboxeslist()
    for semabox in liste_semabox:
        if name == semabox["name"]:
            liste_semabox.remove(semabox)
            with open("semaboxes.json",'w') as f: 
                json.dump(liste_semabox, f, indent=4, separators=(',',': '))
                f.close()
            return True
    return False

@app.route("/")
def home():
    semaboxlist=loadsemaboxeslist()
    print(semaboxlist)
    listedsemaboxes=list(map(operator.itemgetter('name'), semaboxlist))
    print(listedsemaboxes)
    return render_template("index.html", semaboxes=listedsemaboxes)


@app.route('/register', methods =["GET", "POST"])
def registerSemabox():
    if request.method == "POST":
        name=request.form.get("name")
        ip=request.form.get("ip")
        
        try:
            res =requests.post("http://"+ip+":5000/ip", timeout=2)
        except requests.ConnectTimeout:
            flash("ip address is not valid")
            return render_template("flash.html")
        
        liste_semabox=loadsemaboxeslist()
        
        with open("semaboxes.json", "r") as f:
            liste_semabox=json.load(f)
            f.close()
                
            with open("semaboxes.json", "r") as f:
                if f.read(2) != "[]":
                    f.close()
                    for semabox in liste_semabox:
                        if ip == semabox["ip"]:
                            flash("Semabox already registered")
                            return render_template("flash.html")
                else:
                    f.close()
                    with open("semaboxes.json",'w') as f: 
                        liste_semabox.append({"name":name, "ip":ip})
                        json.dump(liste_semabox, f, indent=4, separators=(',',': '))
                        f.close()
                    flash("Semabox registered successfully")
                    return render_template("flash.html")
        
    return render_template("register.html")

@app.route("/semabox/<name>")
def semabox(name):
    semaboxes=loadsemaboxeslist()
    getSemaboxFromList = list(filter(lambda semabox: semabox["name"] == name, semaboxes))
    ip=str(getSemaboxFromList[0]["ip"])
    reshostname = requests.post("http://"+ip+":5000/hostname", timeout=2)
    resOS = requests.post("http://"+ip+":5000/getos", timeout=2)
    return render_template("semabox.html", name=name, hostname=reshostname.text, ip=ip, os=resOS.text)

@app.route("/semabox/<name>/reboot", methods =["GET", "POST"])
def rebootSemabox(name):
    semaboxes=loadsemaboxeslist()
    getSemaboxFromList = list(filter(lambda semabox: semabox["name"] == name, semaboxes))
    ip=str(getSemaboxFromList[0]["ip"])
    res =requests.post("http://"+ip+":5000/reboot", timeout=2)
    flash("Semabox will be rebooted in 1 minute")
    return render_template("flash.html")

@app.route("/semabox/<name>/remove", methods =["GET", "POST"])
def removeSemabox(name):
    deleteSemaboxFromList(name)
    flash("semabox " + name + " removed")
    return render_template("flash.html")
if __name__=='__main__':
   app.run()
   
