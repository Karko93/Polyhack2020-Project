# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 18:45:26 2020

@author: user
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
