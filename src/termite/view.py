import shutil

import termite.colors
from termite.raw import Q_F

cols, rows = shutil.get_terminal_size()
s = ""
for i in range(rows - 1):
    p = str(i+1)
    s += p + " " * (cols - len(p)) + "\n"
print(termite.colors.BG_GREEN(s[:-1]))