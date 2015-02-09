from flask import Flask, render_template, request, session, url_for, escape, redirect
import logins
import os
import datetime
import mail
import math
import json

app = Flask(__name__)

@app.route('/')
def index():
    logged_in = False
    if 'username' in session:
        logged_in = True

    return render_template("index.html", logged_in=logged_in)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('main'))

    error = None

    if request.method == "POST":
        user = request.form['email']
        pasw = request.form['password']
        suc = logins.login(user, pasw)

        if suc:
            session['username'] = user.strip()
            return redirect(url_for('main'))
        else:
            error = "Incorrect credentials"

    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return redirect(url_for('main'))

    error = None

    if request.method == "POST":
        user = request.form['email']
        pasw = request.form['password']
        verf = request.form['verify']

        if len(user) > 2:
            if pasw == verf:
                pk = request.form['key']

                if "PRIVATE" in pk:
                    return "Key must be public you dolt."

                if not mail.key_good(pk):
                    return "Key must be in PEM format."


                suc = logins.register(user, pasw, pk)

                if suc == "Success":
                    session['username'] = user
                    return redirect(url_for('main'))
                else:
                    error = suc

            else:
                error = "Password verification failed."
        else:
            error = "Username must be atleast 3 characters."

    return render_template('register.html', error=error)

@app.route('/main')
def main():
    return redirect(url_for('main_n', page=0))

@app.route('/main/<page>')
def main_n(page=1):
    if not 'username' in session:
        return redirect(url_for('index'))

    try:
        page = int(page)
    except:
        return "Error 500 - /var/www/public_html/FOAD.php Line 69"

    page -= 1

    if page < 0:
        page = 0

    dp = logins.mail_path(logins.uhash(session['username']))
    il = os.listdir(dp)
    if "ID" in il:
        il.remove("ID")

    if "PK" in il:
        il.remove("PK")

    li = [(int(r.split('_')[0]), r) for r in il]
    li = sorted(li, key=lambda li: li[0])
    li = [r[1] for r in li]
    li = li[::-1]

    pgcnt = int(math.ceil(len(li) / 10))

    oi = []

    if page >= pgcnt:
        oi = li[pgcnt*10:]
    else:
        s = page*10
        e = s + 10
        if e > len(li):
            e = len(li)

        oi = li[s:e]

    o = []

    messages = []

    for f in oi:
        fp = dp + "/" + f
        fc = open(fp).read().split('\n')[1:]
        messages.append([
            fc[0], #message
            fc[1], #key
            fc[2], #nonce
            fc[4], #verkey
            fc[3], #ver
            f.split('_')[0], #fid
        ])
        o.append(f.split('_'))

    return render_template("main.html", mail=o, pc=pgcnt+1, messages=messages)

@app.route('/message/<fid>')
def message(fid=None):
    if not 'username' in session:
        return redirect(url_for('index'))

    l = os.listdir(logins.mail_path(logins.uhash(session['username'])))
    path = ""
    o = []

    for f in l:
        if f != "ID" and f != "PK":
            if f.split('_')[0] == fid:
                path = logins.mail_path(logins.uhash(session['username'])) + "/" + f
                break

    if not path:
        return "Can't find message."

    _, enc_msg, enc_key, enc_nonce, ver, enc_ver_key = open(path).read().split('\n')

    return render_template("message.html", msg=enc_msg, key=enc_key, nonce=enc_nonce, ver=ver, ver_key=enc_ver_key)

@app.route("/compose", methods=['POST', 'GET'])
def compose():
    if not 'username' in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        email = request.form['to']

        if '@' not in email:
            return "Not a valid email"

        if email.split('@')[1] != "privatemail.in":
            return "External Hosts not supported for now."

        public = logins.public_key(email.split('@')[0])

        if not public:
            return "User doesn't exist."

        subject = request.form['subject']
        message = request.form['message']
        timestamp = str(datetime.datetime.now()).split('.')[0]

        lines = "From: \"" + session['username'] + "\" <" + session['username'] + "@privatemail.in>\n"
        lines += "To: \"" + email.split('@')[0] + "\" <" + email + ">\n"
        lines += "Date: " + timestamp + "\n"
        lines += "Subject: " + subject + "\n"
        lines += "\n"
        lines += message

        if mail.receive_message(email.split('@')[0], public, lines):
            return redirect(url_for('main'))
        else:
            return "Error."

    return render_template("compose.html")

@app.route("/compose/<name>", methods=['GET'])
def compose_to(name):
    if not 'username' in session:
        return redirect(url_for('index'))

    return render_template("compose.html", name=name)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/delete/<fid>")
def delete(fid=None):
    if not 'username' in session:
        return redirect(url_for('index'))

    l = os.listdir(logins.mail_path(logins.uhash(session['username'])))
    path = ""
    o = []

    for f in l:
        if f != "ID":
            if f.split('_')[0] == fid:
                path = logins.mail_path(logins.uhash(session['username'])) + "/" + f
                break

    if path != "" and os.path.exists(path):
        os.unlink(path)
    else:
        return "Can't find that email."

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.secret_key = '&A*(&SD*9798710289ipoekl;as)'
    #app.run(debug=True, host="127.0.0.1", port=1101)
    app.run(debug=False, host="0.0.0.0", port=1101)
