import os
import sqlite3
import subprocess

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = "cle-secrete-en-dur-123"  # volontaire : secret en dur

DB = "app.db"
UPLOAD_DIR = "uploads"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS serveurs (id INTEGER PRIMARY KEY, nom TEXT, ip TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS secret (flag TEXT)")
    cur.execute("SELECT COUNT(*) FROM serveurs")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO serveurs (nom, ip) VALUES (?, ?)",
            [("web-01", "192.168.1.10"), ("db-01", "192.168.1.11"), ("backup-01", "192.168.1.12")],
        )
        cur.execute("INSERT INTO secret (flag) VALUES (?)", ("FLAG{sqli_table_cachee}",))
    con.commit()
    con.close()


def init_flags():
    # les flags du CTF, poses sur le serveur (lus par les failles ping et upload)
    with open("flag_ping.txt", "w") as f:
        f.write("FLAG{cmd_injection_ping}\n")
    with open("flag_upload.txt", "w") as f:
        f.write("FLAG{upload_execution}\n")


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/recherche")
def recherche():
    q = request.args.get("q", "")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # volontaire : la requete est construite en collant le texte saisi (injection SQL)
    requete = "SELECT nom, ip FROM serveurs WHERE nom = '" + q + "'"
    try:
        cur.execute(requete)
        lignes = cur.fetchall()
    except Exception as e:
        lignes = [("erreur", str(e))]
    con.close()
    return render_template("recherche.html", q=q, lignes=lignes)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = None
    if request.method == "POST":
        f = request.files.get("fichier")
        if f:
            # volontaire : aucun controle du type ni du nom du fichier
            chemin = os.path.join(UPLOAD_DIR, f.filename)
            f.save(chemin)
            message = "Fichier enregistre : " + f.filename
            return render_template("upload.html", message=message, nom=f.filename)
    return render_template("upload.html", message=message, nom=None)


@app.route("/appliquer", methods=["POST"])
def appliquer():
    nom = request.form.get("nom", "")
    # volontaire : l'appli applique la config en executant le fichier depose
    sortie = subprocess.getoutput("sh " + os.path.join(UPLOAD_DIR, nom))
    return render_template("appliquer.html", nom=nom, sortie=sortie)


@app.route("/ping", methods=["GET", "POST"])
def ping():
    sortie = None
    if request.method == "POST":
        hote = request.form.get("hote", "")
        # volontaire : l'adresse saisie est passee a une commande shell (injection de commande)
        sortie = subprocess.getoutput("ping -c 1 " + hote)
    return render_template("ping.html", sortie=sortie)


if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    init_db()
    init_flags()
    # volontaire : mode debug active
    app.run(host="0.0.0.0", port=5000, debug=True)
