import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.load_data()

        # Подключение сигналов к слотам
        self.addButton.clicked.connect(self.add_coffee)
        self.deleteButton.clicked.connect(self.delete_coffee)

    def load_data(self):
        """Загрузка данных из базы данных и отображение их в таблице."""
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.coffeeTable.setRowCount(len(rows))
        self.coffeeTable.setColumnCount(7)  # Учитываем 7 полей в таблице

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.coffeeTable.setItem(i, j, QTableWidgetItem(str(value)))

        connection.close()

    def add_coffee(self):
        """Добавление нового сорта кофе в базу данных."""
        name = self.nameInput.text()
        roast_level = self.roastLevelInput.text()
        grind_type = self.grindTypeInput.text()
        flavor_description = self.flavorDescriptionInput.text()
        price = self.priceInput.text()
        packaging_volume = self.packagingVolumeInput.text()

        if not all([name, roast_level, grind_type, flavor_description, price, packaging_volume]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO coffee (name, roast_level, grind_type, flavor_description, price, packaging_volume) VALUES (?, ?, ?, ?, ?, ?)",
            (name, roast_level, grind_type, flavor_description, price, packaging_volume))
        connection.commit()
        connection.close()

        self.load_data()  # Обновляем таблицу
        self.clear_inputs()  # Очищаем поля ввода

    def delete_coffee(self):
        """Удаление выбранного сорта кофе из базы данных."""
        selected_row = self.coffeeTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите сорт кофе для удаления.")
            return

        coffee_id = self.coffeeTable.item(selected_row, 0).text()  # Получаем ID из первой колонки

        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM coffee WHERE id=?", (coffee_id,))
        connection.commit()
        connection.close()

        self.load_data()  # Обновляем таблицу

    def clear_inputs(self):
        """Очистка полей ввода."""
        self.nameInput.clear()
        self.roastLevelInput.clear()
        self.grindTypeInput.clear()
        self.flavorDescriptionInput.clear()
        self.priceInput.clear()
        self.packagingVolumeInput.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
