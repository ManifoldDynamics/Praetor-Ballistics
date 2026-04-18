with open('gui.py', 'r') as f:
    content = f.read()

content = content.replace("self.stacked_widget.addWidget(menu_widget) # Index 0", "self.stacked_widget.insertWidget(0, menu_widget)")
content = content.replace("self.stacked_widget.addWidget(widget) # Index 1", "self.stacked_widget.insertWidget(1, widget)")
content = content.replace("self.stacked_widget.addWidget(widget) # Index 2", "self.stacked_widget.insertWidget(2, widget)")
content = content.replace("self.stacked_widget.addWidget(widget) # Index 3", "self.stacked_widget.insertWidget(3, widget)")
content = content.replace("self.stacked_widget.addWidget(calc_widget) # Index 1", "self.stacked_widget.insertWidget(4, calc_widget)")
content = content.replace("self.stacked_widget.addWidget(self.aero_widget) # Index 2", "self.stacked_widget.insertWidget(5, self.aero_widget)")

with open('gui.py', 'w') as f:
    f.write(content)
