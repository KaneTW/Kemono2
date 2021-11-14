"""
This folder holds development modules.
Only modules imported to this file are allowed to be imported outside.
These imports always have to be conditional, such as:
```python
if (is_development):
    from development import module_name
    module_name()
```
"""

from .internals import Kemono_Dev, kemono_dev
from .blueprints import development
