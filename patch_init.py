import sys

with open('gui.py', 'r') as f:
    lines = f.readlines()

new_lines = []
in_init = False
for i, line in enumerate(lines):
    if line.startswith("    def __init__(self):"):
        in_init = True
        new_lines.append(line)
        continue

    if in_init and "self.stacked_widget.setCurrentIndex(0)" in line:
        new_lines.append("        self.page_index_main = 0\n")
        new_lines.append("        self.page_index_proj_sel = 1\n")
        new_lines.append("        self.page_index_firearm = 2\n")
        new_lines.append("        self.page_index_proj_des = 3\n")
        new_lines.append("        self.page_index_calc = 4\n")
        new_lines.append("        self.page_index_aero = 5\n")
        new_lines.append(line)
        in_init = False
        continue

    new_lines.append(line)

with open('gui_temp.py', 'w') as f:
    f.writelines(new_lines)
