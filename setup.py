import sys
from cx_Freeze import setup, Executable
import requests.certs

options = {
    "build_exe": {
        "packages": [],
        "excludes": []
    }
}


base = None
if sys.platform == "win32":
    base = "Console"

setup(
    name="PxlsTemplateCreator",
    version="1.1.0",
    description="",
    options=options,
    executables=[Executable("PxlTemplateCreator.py", base=base)]
)
