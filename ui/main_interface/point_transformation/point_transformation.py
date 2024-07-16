from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog, QAbstractItemView
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from .point_transformation_ui import Ui_PointTransformation


class PointTransformation(QWidget):
    def __init__(self, db_file):
        super(PointTransformation, self).__init__()
        self.ui = Ui_PointTransformation()
        self.ui.setupUi(self)
        self.setWindowTitle('Преобразование точек')

        self.db_file = db_file
        self.db = None
        self.open_db()

        self.ui.point_transform.clicked.connect(self.transform)

    def open_db(self):
        if self.db:
            self.close_db()

        self.db = QSqlDatabase.addDatabase('QSQLITE', 'point_db')
        self.db.setDatabaseName(self.db_file)
        if not self.db.open():
            QMessageBox.critical(self, 'Ошибка', 'Ошибка подключения к БД!')

        self.model = QSqlTableModel(db=self.db)
        self.model.setTable('points')
        self.model.select()
        self.ui.point_table.setModel(self.model)
        self.ui.point_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def close_db(self):
        self.ui.point_table.setModel(None)
        del self.model
        self.db.close()
        del self.db
        QSqlDatabase.removeDatabase('point_db')

    def transform(self):
        prefix, ok = QInputDialog.getText(self, 'Префикс', 'Префикс для точек:')
        re = QRegularExpression('^[a-zA-Z0-9]+$')
        if not ok or not re.match(prefix).hasMatch():
            QMessageBox.critical(self, "Ошибка", "Действие отклонено или неправильный префикс (только латинские буквы и цифры)!")
            return

        selection = self.ui.point_table.selectionModel()
        rows = selection.selectedRows(column=0)
        for row in rows:
            query = QSqlQuery()
            query.prepare('UPDATE points SET name = :prefix_name WHERE name LIKE :name')
            query.bindValue(':prefix_name', prefix+row.data())
            query.bindValue(':name', row.data())
            query.exec()

        self.ui.point_table.model().select()
        self.ui.point_table.reset()

    def closeEvent(self, event):
        self.close_db()