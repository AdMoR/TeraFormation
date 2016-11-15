# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

import os
from flask import Flask
from raven.contrib.flask import Sentry
from raven.base import DummyClient
from werkzeug.contrib.fixers import ProxyFix

__title__ = 'Simplon Jobseeker'
__version__ = '0.1'

#
# Creating Flask app object
#
app = Flask(__name__)

#
# Attach Blueprints
#
from .controller import api_v1
app.register_blueprint(api_v1, url_prefix='/v1')