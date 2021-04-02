import threading
import random
import time
import pyrebase
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import TwoLineAvatarListItem, IconLeftWidget
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.app import MDApp



# Firebase Configuration
firebaseConfig = {
    'apiKey': "AIzaSyBQhsn8fWccgdly8bP_br0sIFy7iw0Lsts",
    'authDomain': "onluyentracnghiemk9.firebaseapp.com",
    'databaseURL': "https://onluyentracnghiemk9-default-rtdb.firebaseio.com/",
    'projectId': "onluyentracnghiemk9",
    'storageBucket': "onluyentracnghiemk9.appspot.com",
    'messagingSenderId': "739983860112",
    'appId': "1:739983860112:web:92c642d8856380439c5315",
    'measurementId': "G-QHV5WS8Z82"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

Window.size = (360, 600)

tab_number = 0


class MainLayout(FloatLayout):
    scr_mag = ObjectProperty(None)

    mon_label = StringProperty('')
    waiting_label = StringProperty('')
    time_count = StringProperty('')
    comment = StringProperty('')
    point_label = StringProperty('')
    mon_baithi = StringProperty('')

    text_tn = StringProperty()
    text_xh = StringProperty()
    icon_tn = StringProperty()
    icon_xh = StringProperty()

    time_min = NumericProperty(0)
    prog_val = NumericProperty(0)
    point = 0
    time_baithi = NumericProperty(0)
    get_num = NumericProperty(0)

    mon = ''
    list_mon = []
    array = []
    eng_array = []
    tn_array = []
    xh_array = []
    list3d = []
    m = 0

    stop = False
    change = False
    on_test = False
    string_list = ['Hệ thống đang ra đề. Bạn vui lòng chờ trong giây lát.',
                   'Hệ thống đang ra đề. Bạn vui lòng chờ trong giây lát..',
                   'Hệ thống đang ra đề. Bạn vui lòng chờ trong giây lát...']

    def change_screen(self, screen, *args):
        self.scr_mag.current = screen

    # Dialog chọn môn

    def open_dialog1(self, *args):
        acpt_btn = MDRaisedButton(
            text='Đồng ý', on_release=self.close_dialog1p1)
        canc_btn = MDFlatButton(text='Hủy', on_release=self.close_dialog1)
        self.dialog1 = MDDialog(title='Thông báo', text='Bạn có chắc muốn chọn môn này để ôn luyện không?',
                                buttons=[canc_btn, acpt_btn], size_hint_x=None,
                                width=300)
        self.dialog1.open()

    def close_dialog1(self, *args):
        self.dialog1.dismiss()

    def close_dialog1p1(self, *args):
        self.change_screen('pre_onluyen')
        self.dialog1.dismiss()

    # Dialog chọn thời gian
    def check1(self, time_var, screen, *args):
        ok_btn = MDRaisedButton(text='OK', on_release=self.close_dialog2)
        if time_var > 0:
            self.change_screen(screen)

        else:
            self.dialog2 = MDDialog(title='Thông báo', text='Bạn chưa chọn thời gian!', buttons=[ok_btn],
                                    size_hint_x=None,
                                    width=300)
            self.dialog2.open()

    def close_dialog2(self, *args):
        self.dialog2.dismiss()

    # Dialog nộp bài
    def open_dialog3(self, *args):
        submit_btn = MDRaisedButton(
            text='Nộp bài', on_release=self.close_dialog3p1)
        cancel_btn = MDFlatButton(text='Hủy', on_release=self.close_dialog3)

        self.dialog3 = MDDialog(title='Thông báo', text='Bạn có chắc muốn nộp bài không?',
                                size_hint_x=None, width=300, buttons=[cancel_btn, submit_btn])
        self.dialog3.open()

    def close_dialog3(self, *args):
        self.dialog3.dismiss()

    def close_dialog3p1(self, *args):
        self.stop = True
        self.Marking()
        self.change_screen('finish')
        self.dialog3.dismiss()

    # Dialog nộp bài 2
    def open_dialog4(self, *args):
        smt_btn = MDRaisedButton(
            text='Nộp bài', on_release=self.close_dialog4p1)
        canc_btn = MDFlatButton(text='Hủy', on_release=self.close_dialog4)

        self.dialog4 = MDDialog(title='Thông báo', text='Bạn có chắc muốn nộp bài không?',
                                size_hint_x=None, width=300, buttons=[canc_btn, smt_btn])
        self.dialog4.open()

    def close_dialog4(self, *args):
        self.dialog4.dismiss()

    def close_dialog4p1(self, *args):
        self.stop = True
        self.Marking_BaiThi()
        self.change_screen('finish_baithi')
        self.dialog4.dismiss()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def change_to(self, value):
        global tab_number
        tab_number = value
    # Func chấm điểm

    def Marking(self):
        for i in range(20):
            if self.array[7][i]:
                self.point += 1

        if self.point in range(16, 21):
            self.comment = 'Thật tuyệt vời!'
        elif self.point in range(11, 16):
            self.comment = 'Bạn hãy cố gắng hơn nữa nhé!'
        elif self.point in range(6, 11):
            self.comment = 'Bạn cần nắm vững kiến thức hơn nữa nhé!'
        elif self.point in range(0, 6):
            self.comment = 'Bạn cần ôn lại kiến thức để làm bài tốt hơn nhé!'

        self.point_label = str(self.point)

    def Marking_BaiThi(self):

        for a in range(3):
            for i in range(20):
                if self.list3d[a][7][i]:
                    self.point += 1

        if self.point in range(50, 61):
            self.comment = 'Bài làm của bạn rất tốt! Tiếp tục phát huy bạn nhé!'
        elif self.point in range(20, 50):
            self.comment = 'Bạn hãy ôn luyện thêm để nâng cao kỹ năng bạn nhé!'
        elif self.point in range(0, 20):
            self.comment = 'Bạn cần cần cố gắng hơn nữa nhé!'

        self.point_label = str(self.point)
    # Funcs xử lý loading...

    def MakeQuestion(self, subject, array):
        self.prog_val = 0
        rows, cols = (7, 20)

        # Tạo mảng 2 chiều
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append('')
            array.append(col)

        col = []
        for i in range(20):
            col.append(False)
        array.append(col)

        # Tạo ngẫu nhiên câu hỏi
        dd = []
        for i in range(30):
            dd.append(False)

        k = 0
        while k <= 19:

            num = random.randint(0, 29)
            self.prog_val = k*5+5
            if dd[num] == False:
                dd[num] = True
                num += 1

                options = []

                array[0][k] = db.child(subject).child(
                    'Cau' + str(num)).child('cauhoi').get().val()

                options.append(db.child(subject).child(
                    'Cau' + str(num)).child('optiona').get().val())
                options.append(db.child(subject).child(
                    'Cau' + str(num)).child('optionb').get().val())
                options.append(db.child(subject).child(
                    'Cau' + str(num)).child('optionc').get().val())
                options.append(db.child(subject).child(
                    'Cau' + str(num)).child('optiond').get().val())

                options_index = [0, 1, 2, 3]
                times = random.randint(1, 10)
                count = 1
                while count <= times:
                    r1 = random.randint(0, 3)
                    r2 = random.randint(0, 3)
                    tg = 0

                    while r1 == r2:
                        r2 = random.randint(0, 3)

                    tg = options_index[r1]
                    options_index[r1] = options_index[r2]
                    options_index[r2] = tg

                    count += 1

                # Đưa các options vào mảng array
                array[1][k] = options[options_index[0]]
                array[2][k] = options[options_index[1]]
                array[3][k] = options[options_index[2]]
                array[4][k] = options[options_index[3]]

                array[5][k] = db.child(subject).child(
                    'Cau' + str(num)).child('dapan').get().val()
                k += 1

        if not self.on_test:
            self.change_screen('bailam')
        else:
            self.change_screen('bailam_baithi')

    def Creating_Lists(self):

        threading.Thread(target=self.MakeQuestion, args=[
                         self.list_mon[0], self.eng_array]).start()
        threading.Thread(target=self.MakeQuestion, args=[
                         self.list_mon[1], self.tn_array]).start()
        threading.Thread(target=self.MakeQuestion, args=[
                         self.list_mon[2], self.xh_array]).start()

        self.on_test = True

    def Creating_3D_List(self):
        while True:
            if self.eng_array[5][19] and self.tn_array[5][19] and self.xh_array[5][19] != '':
                self.list3d.append(self.eng_array)
                self.list3d.append(self.tn_array)
                self.list3d.append(self.xh_array)
                return

    def Loading_Label(self):
        y = 0
        while self.prog_val < 100:
            self.waiting_label = self.string_list[y]
            time.sleep(0.5)
            if y == 2:
                y = 0
            else:
                y += 1

    def Loading_Label_Baithi(self):
        y = 0
        while self.on_test:
            self.waiting_label = self.string_list[y]
            time.sleep(0.5)
            if y == 2:
                y = 0
            else:
                y += 1

            if self.scr_mag.current == 'bailam_baithi':
                return

    # Funcs xử lý bài làm

    def CountDownTimer(self, s):

        s *= 60
        while s > 0:
            s
            hour, s2 = divmod(s, 3600)
            minute, sec = divmod(s2, 60)
            self.time_count = '{:02d} : {:02d} : {:02d}'.format(
                hour, minute, sec)

            time.sleep(1)
            s -= 1
            if self.stop:
                return

        self.change_screen('finish')

    def on_tab_switch_3(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if self.list3d != []:
            MainLayout.m = int(tab_text[tab_text.find(' ') + 1:]) - 1
            instance_tab.ids.question.text = self.list3d[tab_number][0][MainLayout.m]
            instance_tab.ids.optiona.text = self.list3d[tab_number][1][MainLayout.m]
            instance_tab.ids.optionb.text = self.list3d[tab_number][2][MainLayout.m]
            instance_tab.ids.optionc.text = self.list3d[tab_number][3][MainLayout.m]
            instance_tab.ids.optiond.text = self.list3d[tab_number][4][MainLayout.m]
            print(MainLayout.m)
        else:
            pass

        if self.list3d != []:
            if self.list3d[tab_number][6][self.m] != '':
                if self.list3d[tab_number][6][self.m] == instance_tab.ids.optiona.text:
                    instance_tab.ids.box1.active = True
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.optionb.text:
                    instance_tab.ids.box2.active = True
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.optionc.text:
                    instance_tab.ids.box3.active = True
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.optiond.text:
                    instance_tab.ids.box4.active = True

    def on_tab_switch_4(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if self.list3d != []:
            self.m = int(tab_text[tab_text.find(' ') + 1:])-1
            instance_tab.ids.question.text = self.list3d[tab_number][0][self.m]
            instance_tab.ids.ans_a.text = self.list3d[tab_number][1][self.m]
            instance_tab.ids.ans_b.text = self.list3d[tab_number][2][self.m]
            instance_tab.ids.ans_c.text = self.list3d[tab_number][3][self.m]
            instance_tab.ids.ans_d.text = self.list3d[tab_number][4][self.m]
        else:
            pass

        if self.list3d != []:
            if self.list3d[tab_number][7][self.m]:
                if self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'check-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'check-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'check-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'check-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (0, 1, 0, 1)
            else:

                if self.list3d[tab_number][5][self.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'check-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][5][self.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'check-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][5][self.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'check-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (0, 1, 0, 1)
                elif self.list3d[tab_number][5][self.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'check-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (0, 1, 0, 1)

                if self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'close-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (1, 0, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'close-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (1, 0, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'close-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (1, 0, 0, 1)
                elif self.list3d[tab_number][6][self.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'close-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (1, 0, 0, 1)
                else:
                    instance_tab.ids.note.text = 'Bạn không chọn câu trả lời cho câu này!'

    def set_text_icon(self):
        switch = {
            'Vật Lý': ('Vật Lý', 'electron-framework'),
            'Hóa Học': ('Hóa Học', 'flask-outline'),
            'Sinh Học': ('Sinh Học', 'dna'),
            'Lịch Sử': ('Lịch Sử', 'castle'),
            'Địa Lý': ('Địa Lý', 'globe-model'),
            'GDCD': ('GDCD', 'head-cog-outline')
        }
        self.text_tn, self.icon_tn = switch.get(
            self.list_mon[1], ('', 'blank'))
        self.text_xh, self.icon_xh = switch.get(
            self.list_mon[2], ('', 'blank'))

    def run_multi_func1(self):
        threading.Thread(target=self.MakeQuestion, args=[
                         self.mon, self.array]).start()
        threading.Thread(target=self.Loading_Label).start()

    def run_multi_func2(self):
        threading.Thread(target=self.CountDownTimer,
                         args=[self.time_min]).start()

    def run_multi_func3(self):
        self.on_test = True
        threading.Thread(target=self.Creating_Lists).start()
        threading.Thread(target=self.Loading_Label_Baithi).start()

    def run_multi_func4(self):
        threading.Thread(target=self.set_text_icon).start()
        threading.Thread(target=self.CountDownTimer,
                         args=[self.time_baithi]).start()
        threading.Thread(target=self.Creating_3D_List).start()


class Tab(FloatLayout, MDTabsBase):
    optiona = ObjectProperty(None)
    optionb = ObjectProperty(None)
    optionc = ObjectProperty(None)
    optiond = ObjectProperty(None)
    box1 = ObjectProperty(None)
    box2 = ObjectProperty(None)
    box3 = ObjectProperty(None)
    box4 = ObjectProperty(None)

    # Funcs checkbox
    def checkA(self, checkbox, active):
        if active:
            MainLayout.array[6][MainLayout.m] = self.optiona.text
        else:
            MainLayout.array[6][MainLayout.m] = ''
        if MainLayout.array[6][MainLayout.m] == MainLayout.array[5][MainLayout.m]:
            MainLayout.array[7][MainLayout.m] = True
        else:
            MainLayout.array[7][MainLayout.m] = False

    def checkB(self, checkbox, active):
        if active:
            MainLayout.array[6][MainLayout.m] = self.optionb.text
        else:
            MainLayout.array[6][MainLayout.m] = ''
        if MainLayout.array[6][MainLayout.m] == MainLayout.array[5][MainLayout.m]:
            MainLayout.array[7][MainLayout.m] = True
        else:
            MainLayout.array[7][MainLayout.m] = False

    def checkC(self, checkbox, active):
        if active:
            MainLayout.array[6][MainLayout.m] = self.optionc.text
        else:
            MainLayout.array[6][MainLayout.m] = ''
        if MainLayout.array[6][MainLayout.m] == MainLayout.array[5][MainLayout.m]:
            MainLayout.array[7][MainLayout.m] = True
        else:
            MainLayout.array[7][MainLayout.m] = False

    def checkD(self, checkbox, active):
        if active:
            MainLayout.array[6][MainLayout.m] = self.optiond.text
        else:
            MainLayout.array[6][MainLayout.m] = ''
        if MainLayout.array[6][MainLayout.m] == MainLayout.array[5][MainLayout.m]:
            MainLayout.array[7][MainLayout.m] = True
        else:
            MainLayout.array[7][MainLayout.m] = False


class TabBaiThi(FloatLayout, MDTabsBase):
    optiona = ObjectProperty(None)
    optionb = ObjectProperty(None)
    optionc = ObjectProperty(None)
    optiond = ObjectProperty(None)
    box1 = ObjectProperty(None)
    box2 = ObjectProperty(None)
    box3 = ObjectProperty(None)
    box4 = ObjectProperty(None)

    def checkA(self, checkbox, active):
        if active:
            MainLayout.list3d[tab_number][6][MainLayout.m] = self.optiona.text
            print(tab_number)
            print(MainLayout.list3d[0][6])
            print(MainLayout.list3d[1][6])
            print(MainLayout.list3d[2][6])

        else:
            MainLayout.list3d[tab_number][6][MainLayout.m] = ''
        if MainLayout.list3d[tab_number][6][MainLayout.m] == MainLayout.list3d[tab_number][5][MainLayout.m]:
            MainLayout.list3d[tab_number][7][MainLayout.m] = True
        else:
            MainLayout.list3d[tab_number][7][MainLayout.m] = False

    def checkB(self, checkbox, active):
        if active:
            MainLayout.list3d[tab_number][6][MainLayout.m] = self.optionb.text
            print(tab_number)
            print(MainLayout.list3d[0][6])
            print(MainLayout.list3d[1][6])
            print(MainLayout.list3d[2][6])

        else:
            MainLayout.list3d[tab_number][6][MainLayout.m] = ''
        if MainLayout.list3d[tab_number][6][MainLayout.m] == MainLayout.list3d[tab_number][5][MainLayout.m]:
            MainLayout.list3d[tab_number][7][MainLayout.m] = True
        else:
            MainLayout.list3d[tab_number][7][MainLayout.m] = False

    def checkC(self, checkbox, active):
        if active:
            MainLayout.list3d[tab_number][6][MainLayout.m] = self.optionc.text
            print(tab_number)
            print(MainLayout.list3d[0][6])
            print(MainLayout.list3d[1][6])
            print(MainLayout.list3d[2][6])

        else:
            MainLayout.list3d[tab_number][6][MainLayout.m] = ''
        if MainLayout.list3d[tab_number][6][MainLayout.m] == MainLayout.list3d[tab_number][5][MainLayout.m]:
            MainLayout.list3d[tab_number][7][MainLayout.m] = True
        else:
            MainLayout.list3d[tab_number][7][MainLayout.m] = False

    def checkD(self, checkbox, active):
        if active:
            MainLayout.list3d[tab_number][6][MainLayout.m] = self.optiond.text
            print(tab_number)
            print(MainLayout.list3d[0][6])
            print(MainLayout.list3d[1][6])
            print(MainLayout.list3d[2][6])

        else:
            MainLayout.list3d[tab_number][6][MainLayout.m] = ''
        if MainLayout.list3d[tab_number][6][MainLayout.m] == MainLayout.list3d[tab_number][5][MainLayout.m]:
            MainLayout.list3d[tab_number][7][MainLayout.m] = True
        else:
            MainLayout.list3d[tab_number][7][MainLayout.m] = False


class TabReview(FloatLayout, MDTabsBase):
    ans_a = ObjectProperty(None)
    ans_b = ObjectProperty(None)
    ans_c = ObjectProperty(None)
    ans_d = ObjectProperty(None)
    icon1 = ObjectProperty(None)
    icon2 = ObjectProperty(None)
    icon3 = ObjectProperty(None)
    icon4 = ObjectProperty(None)
    noti_label = StringProperty('')


class TabBaiThiReview(FloatLayout, MDTabsBase):
    ans_a = ObjectProperty(None)
    ans_b = ObjectProperty(None)
    ans_c = ObjectProperty(None)
    ans_d = ObjectProperty(None)
    icon1 = ObjectProperty(None)
    icon2 = ObjectProperty(None)
    icon3 = ObjectProperty(None)
    icon4 = ObjectProperty(None)
    noti_label = StringProperty('')


class ContentBaiThi(FloatLayout):
    pass


class ContentOnLuyen(FloatLayout):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass

    # Func khởi tạo Tab
    def on_start(self):
        for i in range(1, 21):
            self.root.ids.tabs.add_widget(Tab(text=f'Câu {i}'))
            self.root.ids.tabs2.add_widget(TabReview(text=f'Câu {i}'))
            self.root.ids.tabs_baithi1.add_widget(TabBaiThi(text=f'Câu {i}'))
            self.root.ids.tabs_baithi2.add_widget(TabBaiThi(text=f'Câu {i}'))
            self.root.ids.tabs_baithi3.add_widget(TabBaiThi(text=f'Câu {i}'))
            self.root.ids.tabs_baithi4.add_widget(
                TabBaiThiReview(text=f'Câu {i}'))
            self.root.ids.tabs_baithi5.add_widget(
                TabBaiThiReview(text=f'Câu {i}'))
            self.root.ids.tabs_baithi6.add_widget(
                TabBaiThiReview(text=f'Câu {i}'))

    # Func tạo nội dung và đánh dấu checkbox cho Tab chọn

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if MainLayout.array != []:
            MainLayout.m = int(tab_text[tab_text.find(' ') + 1:])-1
            instance_tab.ids.question.text = MainLayout.array[0][MainLayout.m]
            instance_tab.ids.optiona.text = MainLayout.array[1][MainLayout.m]
            instance_tab.ids.optionb.text = MainLayout.array[2][MainLayout.m]
            instance_tab.ids.optionc.text = MainLayout.array[3][MainLayout.m]
            instance_tab.ids.optiond.text = MainLayout.array[4][MainLayout.m]

        else:
            pass
        if MainLayout.array != []:
            if MainLayout.array[6][MainLayout.m] != '':
                if MainLayout.array[6][MainLayout.m] == instance_tab.ids.optiona.text:
                    instance_tab.ids.box1.active = True
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.optionb.text:
                    instance_tab.ids.box2.active = True
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.optionc.text:
                    instance_tab.ids.box3.active = True
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.optiond.text:
                    instance_tab.ids.box4.active = True

    def on_tab_switch_2(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if MainLayout.array != []:
            MainLayout.m = int(tab_text[tab_text.find(' ') + 1:])-1
            instance_tab.ids.question.text = MainLayout.array[0][MainLayout.m]
            instance_tab.ids.ans_a.text = MainLayout.array[1][MainLayout.m]
            instance_tab.ids.ans_b.text = MainLayout.array[2][MainLayout.m]
            instance_tab.ids.ans_c.text = MainLayout.array[3][MainLayout.m]
            instance_tab.ids.ans_d.text = MainLayout.array[4][MainLayout.m]

        else:
            pass

        if MainLayout.array != []:
            if MainLayout.array[7][MainLayout.m]:
                if MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'check-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (0, 1, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'check-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (0, 1, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'check-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (0, 1, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'check-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (0, 1, 0, 1)
            else:

                if MainLayout.array[5][MainLayout.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'check-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (0, 1, 0, 1)
                elif MainLayout.array[5][MainLayout.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'check-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (0, 1, 0, 1)
                elif MainLayout.array[5][MainLayout.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'check-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (0, 1, 0, 1)
                elif MainLayout.array[5][MainLayout.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'check-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (0, 1, 0, 1)

                if MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_a.text:
                    instance_tab.ids.icon1.icon = 'close-circle'
                    instance_tab.ids.icon1.theme_text_color = 'Custom'
                    instance_tab.ids.icon1.color = (1, 0, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_b.text:
                    instance_tab.ids.icon2.icon = 'close-circle'
                    instance_tab.ids.icon2.theme_text_color = 'Custom'
                    instance_tab.ids.icon2.color = (1, 0, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_c.text:
                    instance_tab.ids.icon3.icon = 'close-circle'
                    instance_tab.ids.icon3.theme_text_color = 'Custom'
                    instance_tab.ids.icon3.color = (1, 0, 0, 1)
                elif MainLayout.array[6][MainLayout.m] == instance_tab.ids.ans_d.text:
                    instance_tab.ids.icon4.icon = 'close-circle'
                    instance_tab.ids.icon4.theme_text_color = 'Custom'
                    instance_tab.ids.icon4.color = (1, 0, 0, 1)
                else:
                    instance_tab.ids.note.text = 'Bạn không chọn câu trả lời cho câu này!'

    # Xóa tab đầu

    def remove_first_tab(self):
        self.root.ids.tabs.remove_widget(self.root.ids.tabs.get_tab_list()[20])

    # Xóa tab đầu 2
    def remove_first_tab_2(self):
        self.root.ids.tabs2.remove_widget(
            self.root.ids.tabs2.get_tab_list()[20])

    def remove_first_tab_3(self):
        self.root.ids.tabs_baithi1.remove_widget(
            self.root.ids.tabs_baithi1.get_tab_list()[20])
        self.root.ids.tabs_baithi2.remove_widget(
            self.root.ids.tabs_baithi2.get_tab_list()[20])
        self.root.ids.tabs_baithi3.remove_widget(
            self.root.ids.tabs_baithi3.get_tab_list()[20])

    def remove_first_tab_4(self):
        self.root.ids.tabs_baithi4.remove_widget(
            self.root.ids.tabs_baithi4.get_tab_list()[20])
        self.root.ids.tabs_baithi5.remove_widget(
            self.root.ids.tabs_baithi5.get_tab_list()[20])
        self.root.ids.tabs_baithi6.remove_widget(
            self.root.ids.tabs_baithi6.get_tab_list()[20])


if __name__ == '__main__':
    MainApp().run()
