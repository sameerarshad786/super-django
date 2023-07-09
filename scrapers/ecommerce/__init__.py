import sys
import os
import django


sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'super_social.settings'
django.setup()

from .ebay_source import *
from .daraz_source import *
