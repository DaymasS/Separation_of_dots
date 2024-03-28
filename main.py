# Еникеев Тимур ИУ7-24Б
# Нахождение прямой на плоскости, разделяющей множество
# точек на примерно равные группы

# Алгорит Брезенхема

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QAction, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QMouseEvent, QPixmap, QImage
from PyQt5 import uic

from seak_line import search_line

Form, Window = uic.loadUiType("graph.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

crds_table = window.findChild(QTableWidget, "table_crds")
calc_btn = window.findChild(QPushButton, "pBtn_calc")
clear_btn = window.findChild(QPushButton, "pBtn_clear")
del_line_btn = window.findChild(QPushButton, "pBtn_del_line")
img = window.findChild(QLabel, "img")
about_btn = window.findChild(QAction, "about")

crds_list = [(None, None)]

def rise_about():
    msg = QMessageBox()
    msg.setWindowTitle("About")
    msg.setText("Program was developed by Timur Enikeev IU7-24Б.\n" +
                "The app builds a line that seperates dots to two equal groups.\n" +
                "The dots can be placed by clicking on the blues filed or by entering their posiotion.")

    msg.exec()

def img_clicked(event):
    x = event.pos().x()
    y = img.size().height() - event.pos().y() - 1
    update_table(values=(int(x), int(y)))

def check_row(values):
    upper_bound = 1300
    lower_bound = 0
    updated_values = (None, None)
    try:
        updated_values = (int(values[0]), int(values[1]))
    except ValueError:
        return (1, updated_values)
    if not (updated_values[0] < upper_bound and updated_values[0] > lower_bound 
            and updated_values[1] < upper_bound and updated_values[1] > lower_bound):
        return (2, (None, None))    
    return (0, updated_values)

def draw_dots(crds_list):
    empty_tup = (None, None)
    px = QPixmap(img.size().height(), img.size().width())
    px.fill(QColor("Light blue"))
    temp_img = px.toImage()
    for elem in crds_list:
        if not(elem is empty_tup):
            fixed_elem = (elem[0], img.size().height() - elem[1] - 1)
            for i in range(-5, 5):
                for j in range(-5, 5):
                    if (fixed_elem[1] + j < img.size().height() and fixed_elem[1] + j >= 0 and fixed_elem[0] + i < img.size().width() and fixed_elem[0] + i >= 0):
                        temp_img.setPixelColor(fixed_elem[0] + i, fixed_elem[1] + j, QColor("Red"))
    px = QPixmap.fromImage(temp_img)
    img.setPixmap(px)
    


def update_table(*items, values=None, hard_reset=False):
    empty_tup = (None, None)
    num_of_rows = len(crds_list)
    is_list_changed = False
    if not(values is None):
        is_list_changed = True
        if (values in crds_list):
            index = crds_list.index(values)
            crds_list.pop(index)
            crds_table.removeRow(index)
        else:
            crds_table.setItem(num_of_rows - 1, 0, QTableWidgetItem(str(values[0])))
            crds_table.setItem(num_of_rows - 1, 1, QTableWidgetItem(str(values[1])))
            crds_list[num_of_rows - 1] = values
    
    i = 0
    while (i < num_of_rows):
        if (crds_table.item(i, 0) is None or crds_table.item(i, 1) is None):
            i += 1
            continue
        if (i != num_of_rows - 1 and crds_table.item(i, 0).text() == "" and crds_table.item(i, 1).text() == ""):
            crds_list.pop(i)
            crds_table.removeRow(i)
            num_of_rows -= 1
            is_list_changed = True
            continue
        
        if (crds_table.item(i, 0).text() == "" or crds_table.item(i, 1).text() == ""):
            if not (crds_list[i] is None):
                crds_list[i] = empty_tup
                is_list_changed = True
        else:
            r_c, values = check_row((crds_table.item(i, 0).text(), crds_table.item(i, 1).text()))
            if (r_c == 0):
                if (values != crds_list[i]):
                    crds_list[i] = values
                    is_list_changed = True
                    if (i == num_of_rows - 1):
                        crds_table.setRowCount(num_of_rows + 1)
                        crds_list.append(empty_tup)
        i += 1

    if (is_list_changed or hard_reset):
        draw_dots(crds_list)

def fix_crds(crds_list):
    fixed_crds = []
    for elem in crds_list:
        if (elem != (None, None)):
            fixed_crds.append(elem)
    return fixed_crds

def draw_line(k, b):
    px = img.pixmap()
    temp_img = px.toImage()
    if (k != None):
        y_prev = b
        for x in range(3, img.size().width() - 3):
            y = int(k * x + b)
            if (abs(y - y_prev) > 7 and (y >= 0 and y < img.size().height() or y_prev >= 0 and y_prev < img.size().height())):
                step = 1
                if (y < y_prev):
                    step = -step
                while (abs(y_prev - y) > 7):
                    for i in range(-3, 4):
                        x_draw = x + i
                        if (y_prev < img.size().height() and y_prev >= 0 and x_draw < img.size().width() and x_draw >= 0):
                            temp_img.setPixelColor(x_draw, img.size().height() - y_prev - 1, QColor("Green"))
                    y_prev += step
            else:
                y_prev = y
            for j in range(-3, 4):
                for i in range(-3, 4):
                    y_draw = y + i
                    x_draw = x + j
                    if (y_draw >= 0 and y_draw < img.size().height()):
                        temp_img.setPixelColor(x_draw, img.size().height() - y_draw - 1, QColor("Green"))
    else:
        for y in range(3, img.size().height() - 2):
            for i in range(-3, 4):
                x_draw = b + i
                if (x_draw >= 0 and x_draw < img.size().width()):
                    temp_img.setPixelColor(x_draw, y, QColor("Green"))

    px = QPixmap.fromImage(temp_img)
    img.setPixmap(px)


def calc_btn_clicked():
    fixed_crds = fix_crds(crds_list)
    r_c, k, b = search_line(fixed_crds)
    if (r_c == 0):
        draw_line(k, b)
    
def clear_btn_clicked():
    global crds_list
    crds_list = [(None, None)]
    crds_table.setRowCount(0)
    crds_table.setRowCount(1)
    update_table(hard_reset=True)

def del_line_btn_clicked():
    update_table(hard_reset=True)

img.mousePressEvent = img_clicked
crds_table.itemChanged.connect(update_table)
about_btn.triggered.connect(rise_about)
calc_btn.clicked.connect(calc_btn_clicked)
clear_btn.clicked.connect(clear_btn_clicked)
del_line_btn.clicked.connect(del_line_btn_clicked)
draw_dots(crds_list)

window.show()
app.exec()
