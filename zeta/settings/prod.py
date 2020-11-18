# PRODUCTION Settings

import os
from zeta.settings.base import *
import dj_database_url

DEBUG = False

DATABASES["default"] = dj_database_url.parse(
    os.getenv("DATABASE_URL"), conn_max_age=600
)
