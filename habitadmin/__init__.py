# -*- coding: utf-8 -*-
import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create application
app = Flask(__name__)

# Settings
app.config.from_pyfile('settings.cfg', silent=True)

from controllers import actions
