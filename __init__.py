#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, render_template, redirect

from sqlconnect import MyPigFarm, MyPig

app = Flask(__name__)

db = MyPigFarm()
docs = MyPig(db, 'main')


@app.route('/')
def index():
    try:
        table = docs.select([0,1,2,3,6], '', 'ID DESC')
        return render_template("docoversikt.html", table=table)
    except Exception as e:
        return render_template('flash.html', text=e)


@app.route('/nyttdokument')
def nytt_dokument():
    return render_template('nyttdokument.html')


@app.route('/display')
def display():

    row = request.args.get('row')
    doc = docs.select([0,1,3,4], row)

    return render_template("textedit.html", doc=doc)

@app.route('/flash', methods=['POST'])
def flash_text():
    try:    
        text = request.form['myeditablediv']

        return render_template('flash.html', text=text)
    except Exception as e:
        return render_template('flash.html', text=e)


# --------------- POSTS ----------------

@app.route('/opprett', methods=['POST'])
def opprett():
    try:
        success = docs.opprett_dokument(request.form)

        return redirect(url_for('index'))
    except Exception as e: 
        return render_template('flash.html', text=e)


@app.route('/textupdate', methods=['POST'])
def textupdate():
    try:
        text = request.form['myeditablediv']
        row_id = request.form['ID']
        success = docs.rowupdate(['Text'], [text], row_id)

        return redirect(url_for('index'))
    except Exception as e:
        return render_template('flash.html', text=e)


if __name__ == "__main__":
    app.run()
