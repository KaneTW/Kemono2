"""
Environment variable assignments are stored there.
No transformation allowed, therefore all variables there are strings.
"""

import os

flask_env = os.getenv('FLASK_ENV', 'development')
archiver_host = os.getenv('ARCHIVERHOST')
archiver_port = os.getenv('ARCHIVERPORT', '8000')
