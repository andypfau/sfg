# The sample files are supposed to be called from the root folder of
#   the repo. This script ensures the library folder is found, and
#   also that an empty folder <output> is created for the generated
#   files.

import sys
import os

sys.path.insert(0, '.')
os.makedirs('./output')
