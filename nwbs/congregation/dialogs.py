from PyQt6.QtWidgets import (QVBoxLayout, QMessageBox, 
QDialog, QDialogButtonBox, QLineEdit, QComboBox, 
QFormLayout
)

class addDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Add Publisher")
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.setup_ui()
	
	def setup_ui(self):
		'''Setup the add publishers'''
		self.fname_input = QLineEdit()
		self.fname_input.setObjectName("name_input")
		self.fname_input.setMinimumSize(300, 30)
		self.mname_input = QLineEdit()
		self.mname_input.setObjectName("mname_input")
		self.mname_input.setMinimumSize(300, 30)
		self.lname_input = QLineEdit()
		self.lname_input.setObjectName("lname_input")
		self.lname_input.setMinimumSize(300, 30)
		self.role = QComboBox()
		self.role.setObjectName("role_input")
		self.role.setMinimumSize(300, 30)
		self.role.addItems(["Publisher","Ministerial Servant", "Elder"])

		layout = QFormLayout()
		layout.addRow("First Name", self.fname_input)
		layout.addRow("Middle Name (Optional)", self.mname_input)
		layout.addRow("Last Name", self.lname_input)
		layout.addRow("Role", self.role)

		self.layout.addLayout(layout)
		self.button_box = QDialogButtonBox(self)
		self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		self.layout.addWidget(self.button_box)
	
	def accept(self):
		'''Accept data and cary validations'''
		self.data = []
		for publisher in (self.fname_input, self.mname_input, self.lname_input):
			if not publisher.text():
				if publisher.objectName() == "mname_input":
					self.data.append(publisher.text())
					continue
				QMessageBox.critical(self, "Notification", f"You need to enter {publisher.objectName()} field")
				self.data = None # reset data
				return
			self.data.append(publisher.text())

		if not self.role.currentText():
			QMessageBox.critical(self, "Notification", "You need to select a role")
			self.data = None
		
		self.data.append(self.role.currentText())

		if not self.data:
			return

		super().accept()