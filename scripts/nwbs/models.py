from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel

class PublisherModel:
    def __init__(self):
        self.model = self._create_model()
    
    @staticmethod
    def _create_model():
        # learn more here https://realpython.com/python-contact-book/#reader-comments
        model = QSqlTableModel()
        model.setTable('congregation_publishers')
        model.select()
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        headers = ("ID","First Name", "Middle Name", "Last Name", "Role")
        for col_index, header in enumerate(headers):
            model.setHeaderData(col_index, Qt.Orientation.Horizontal, header)
        return model
    
    def add_publisher(self, data:list):
        '''Add publishers to database'''
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for col_index, data_field in enumerate(data):
            self.model.setData(self.model.index(rows, col_index + 1), data_field)
        self.model.submitAll()
        self.model.select()
    
    def delete_publisher(self, index_position:int):
        '''Delete a publisher from database'''
        self.model.removeRow(index_position)
        self.model.submitAll()
        self.model.select()