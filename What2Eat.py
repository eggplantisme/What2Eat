import os
import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QStringListModel
import What2EatUI
from functools import partial

class Meal:
    def __init__(self) -> None:
        self.meals = []
        self.path = './What2Eat.list'
    
    def loadMenu(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    self.meals.append(line.strip())
    
    def saveMenu(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            for meal in self.meals:
                f.write(meal)
                f.write('\n')
    
    def addMeal(self, meal):
        self.meals.append(meal)
    
    def deleteMeal(self, meal):
        if meal is None:
            print("Input Meal Wrong!")
        elif type(meal) is int:
            if 0 <= meal < len(self.meals):
                self.meals.pop(meal)
        else:
            if meal in self.meals:
                self.meals.remove(meal)
    
    def randomChoose(self):
        if len(self.meals) <= 0:
            return "寂寞"
        i = random.randint(0, len(self.meals) - 1)
        return self.meals[i]

def cmdMain():
    meal = Meal()
    meal.loadMenu()
    description = "*" * 17 + '\n* add -    加菜 *\n' + '\n* list -   列菜 *\n' + '\n* delete - 删菜 *\n' + '\n* get -    选菜 *\n' + '\n* exit -   结束 *\n' + "*" * 17 + '\n'
    print(description)
    command = input("请输入指令：")
    while command != 'exit':
        if command == 'add':
            m = input("请加菜：")
            meal.addMeal(m)
            meal.saveMenu()
            print()
        elif command == 'list':
            for i, m in enumerate(meal.meals):
                if i % 3 == 2:
                    print(str(i) + '. ' + m)
                else:
                    print(str(i) + '. ' + m, end='\t')
            print()
        elif command == "delete":
            m = input('请删菜(名字或id)')
            if m.isdigit():
                m = int(m)
            meal.deleteMeal(m)
            meal.saveMenu()
            print()
        elif command == 'get':
            print("咱就吃~" + meal.randomChoose() + '!')
            print()
        else:
            pass
        command = input("请输入指令：")


def addMeal(ui, meal):
    inputMeal = ui.lineEdit.text()
    if "".join(inputMeal.split()) != "":
        meal.addMeal(inputMeal)
        meal.saveMenu()
        listMeal(ui, meal)
        ui.lineEdit.setText("")


def deleteMeal(ui, meal):
    inputMeal = ui.lineEdit_2.text()
    if "".join(inputMeal.split()) != "":
        if inputMeal.isdigit():
                inputMeal = int(inputMeal)
        meal.deleteMeal(inputMeal)
        meal.saveMenu()
        listMeal(ui, meal)
        ui.lineEdit_2.setText("")


def selectMeal(ui, meal):
    m = meal.randomChoose()
    output = "咱就吃这~~~" + m
    ui.textBrowser.setText(output)


def listMeal(ui, meal):
    mealListModel = QStringListModel()
    mealListModel.setStringList([str(i) + '. ' + m for i, m in enumerate(meal.meals)])
    ui.listView.setModel(mealListModel)


def QTMain():
    meal = Meal()
    meal.loadMenu()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = What2EatUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # LIST
    listMeal(ui, meal)
    ui.pushButton.clicked.connect(partial(addMeal, ui, meal))
    ui.pushButton_2.clicked.connect(partial(deleteMeal, ui, meal))
    ui.pushButton_3.clicked.connect(partial(selectMeal, ui, meal))
    sys.exit(app.exec_())


if __name__ == '__main__':
    QTMain()
