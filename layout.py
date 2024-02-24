import os
import pickle
import sys
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import datetime as dt
from PySide6.QtWidgets import QVBoxLayout, QLineEdit, QFileDialog, QLabel
btn_type = Qw.QMessageBox.StandardButton
sp_exp = Qw.QSizePolicy.Policy.Expanding



class change_name(Qw.QWidget):
    def __init__(self):
        super().__init__()

        self.data_file = 'template_list.pkl'
        self.data_name_file = 'template_name_list.pkl'
        self.template_list = self.load_list(self.data_file)
        self.template_name_list = self.load_list(self.data_name_file)


        self.setWindowTitle("change name")
        self.setGeometry(0, 0, 1100, 400)

        change_name_layout = QVBoxLayout(Qw.QWidget(self))

        #読み込んでいるファイル
        self.file_name = QLabel("選択されているファイルなし")
        self.file_name.setFixedSize(1000,50)
        change_name_layout.addWidget(self.file_name)

        #テキストボックス
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("新しい名前(拡張子を除く)")
        change_name_layout.addWidget(self.text_box)

        #ファイル選択ボタンの表示
        self.botton_open_file = Qw.QPushButton("ファイルの選択",self)
        self.botton_open_file.setFixedSize(100, 50)
        self.botton_open_file.clicked.connect(self.botton_open_file_clicked)
        change_name_layout.addWidget(self.botton_open_file)

        #名前変更ボタンの表示
        self.botton_rename = Qw.QPushButton("ファイル名の変更",self)
        self.botton_rename.setFixedSize(100, 50)
        self.botton_rename.clicked.connect(self.botton_rename_clicked)
        self.botton_rename.move(110,92)
        change_name_layout.addWidget(self.botton_open_file)

        #テンプレートコンボボックス
        self.template_combo_pref = Qw.QComboBox(self)
        self.template_combo_pref.setGeometry(212,92,100,49)
        self.template_combo_pref.setEditable(False)
        for p in self.template_list:
            self.template_combo_pref.addItem(p)
        self.template_combo_pref.setCurrentIndex(len(self.template_list)-1)

        #テンプレートの検証ラベル
        self.label_pref_vm = Qw.QLabel(self)
        self.label_pref_vm.setGeometry(400,10,400,80)
        self.label_pref_vm.setVisible(True)

        #テンプレートのリストの内容を貼り付けるボタン
        self.pasteButton = Qw.QPushButton("テンプレートをペースト",self)
        self.pasteButton.clicked.connect(self.paste_to_chname)
        self.pasteButton.setGeometry(312,92,120,49)


    def load_list(self, file_path):
        try:
            with open (file_path, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []
        
    def save_list(self, file_path, data):
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)



    
    def botton_open_file_clicked(self):
        title = '通常のファイルを開く' 
        init_path = os.path.expanduser('~/Desktop')
        filter = 'All Files(*)'
        self.path, _ = Qw.QFileDialog.getOpenFileName(
                self,      # 親ウィンドウ
                title,     # ダイアログタイトル
                init_path, # 初期位置（フォルダパス）
                filter)    # 拡張子によるフィルタ
        print(f'path => "{self.path}"')  # 確認

        if self.path:  
            self.file_name.setText(f"{self.path}")
            self.file_name, self.file_extension = os.path.splitext(self.path)
            print(self.file_extension)
            print(self.file_name)

    #名前変更処理
    def botton_rename_clicked(self):
        new_name = self.text_box.text()
        if hasattr(self, 'path') and self.text_box.text():
            directory = os.path.dirname(self.path)
            new_file_name = os.path.join(directory, new_name + self.file_extension)
            before_change = os.path.join(directory, self.file_name + self.file_extension)
            newFilePath = os.path.join(directory, new_name)
            os.rename(before_change, new_file_name)
            self.file_name.setText(f"ファイル名変更完了： {newFilePath}")
            self.path = new_file_name

    #名前をテキストボックスに貼り付け
    def paste_to_chname(self):
        #選択されているコンボボックスがリストの何番目かを探す
        selected_index = self.template_combo_pref.currentIndex()
        #リストの指定した内容を取得
        if len(self.template_name_list) > 0:
            name = self.template_name_list[selected_index]
            #テキストをペースト
            self.text_box.setText(name)

class Template_registration(Qw.QWidget):
    def __init__(self):

        super().__init__()

        
        self.data_file = 'template_list.pkl'
        self.data_name_file = 'template_name_list.pkl'
        self.template_list = []
        self.template_name_list = []

        Template_registration_layout = QVBoxLayout(Qw.QWidget(self))
        self.setWindowTitle("Template registration")
        self.setGeometry(0,0,500,500)

        #テンプレートとして登録する際の名前
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("テンプレートとして登録する際の名前(例：国語)")
        Template_registration_layout.addWidget(self.text_box)

        #テキストボックス
        self.txt_box_log = Qw.QTextEdit('')
        self.txt_box_log.setPlaceholderText('(テンプレートに登録したいファイル名を入力)')
        self.txt_box_log.setMinimumSize(20,100)
        self.txt_box_log.setSizePolicy(sp_exp,sp_exp)
        Template_registration_layout.addWidget(self.txt_box_log)
        
        #登録確定ボタン
        self.button_Determine_registration = Qw.QPushButton("登録確定", self)
        self.button_Determine_registration.setGeometry(10,230,150,25)
        self.button_Determine_registration.clicked.connect(self.add_Determine_registration)


    def add_Determine_registration(self):
        
        
        #テキスト内容を取得

        self.data_file = 'template_list.pkl'
        self.data_name_file = 'template_name_list.pkl'
        self.template_list = self.load_list(self.data_file)
        self.template_name_list = self.load_list(self.data_name_file)

        text_title = self.text_box.text()
        text_name = self.txt_box_log.toPlainText()

        #リストにテンプレートの名前の項目を追加
        self.template_list.append(text_title)
        self.text_box.clear()
        #リストに名前を登録
        self.template_name_list.append(text_name)
        self.txt_box_log.clear() 

        self.save_list(self.data_file, self.template_list)
        self.save_list(self.data_name_file, self.template_name_list)

        print(self.template_name_list)


        
    def save_list(self, file_path, data):
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)

    def load_list(self, file_path):
        try:
            with open (file_path, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []


class MainWindow(Qw.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.initUI(app)


    def initUI(self, app):
        

        # QRectオブジェクトのインスタンスを作成
        rect = Qc.QRect(0, 0, 480, 100)

        # 画面の中央座標を計算
        centerPoint = app.primaryScreen().availableGeometry().center()
        rect.moveCenter(centerPoint)

        # ウィンドウのジオメトリを設定
        self.setGeometry(rect)

        # 中央のウィジェットとレイアウトの設定
        central_widget = Qw.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        #名称変更ボタン
        self.button_chname = Qw.QPushButton("名称変更", self)

        self.button_chname.setFixedSize(100, 50)

        self.button_chname.clicked.connect(self.open_change_name)
        main_layout.addWidget(self.button_chname)

        self.setCentralWidget(self.button_chname)

        #テンプレート
        self.button_Template_registration = Qw.QPushButton("テンプレート登録", self)
        self.button_Template_registration.setGeometry(100,0,100,50)
        self.button_Template_registration.clicked.connect(self.open_Template_registration)


    def open_change_name(self):
        self.change_name = change_name()  

        mainWindowGeometry = self.geometry()


        #名称変更機能の位置調整
        x = mainWindowGeometry.x() + mainWindowGeometry.width() + 20
        y = mainWindowGeometry.y() + mainWindowGeometry.height() + 20
        
        #名称変更ウィンドウの出現
        self.change_name.move(x, y)
        self.change_name.show()

    def open_Template_registration(self):

        self.Template_registration = Template_registration()

        mainWindowGeometry = self.geometry()
        x = mainWindowGeometry.x() + mainWindowGeometry.width() + 40
        y = mainWindowGeometry.y() + mainWindowGeometry.height() + 40

        self.Template_registration.move(x, y)
        self.Template_registration.show()