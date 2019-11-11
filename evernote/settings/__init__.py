import os
from .base import *

# Загружаем разные конфиги
try:

    try:
        from .local import *
        print("Loaded local config.")

    except ImportError as e:
        from .dev import *
        print("Loaded dev config.")

except:
    print("Loaded base config")
