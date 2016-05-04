#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("docoversikt.html")

@app.route('/display')
def display():
    return render_template("textedit.html")

if __name__ == "__main__":
	app.run()
