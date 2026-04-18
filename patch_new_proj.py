import sys

with open('gui.py', 'r') as f:
    content = f.read()

old_func = """    def new_project(self):
        self.project = BallisticsProject()
        self.populate_gui_from_project()
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("Wilson Ballistic Suite - New Project")"""

new_func = """    def new_project(self):
        self.project = BallisticsProject()
        self.populate_gui_from_project()
        # Navigate to the new Projectile Selection screen instead of calculator
        self.stacked_widget.setCurrentIndex(self.page_index_proj_sel)
        self.setWindowTitle("Wilson Ballistic Suite - New Project")"""

content = content.replace(old_func, new_func)

with open('gui.py', 'w') as f:
    f.write(content)
