import sys
from datetime import datetime
from ultralytics.utils.id_utils import get_id_info, sava_id_info # 账号信息工具函数
from lib.share import shareInfo # 公共变量名
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

# 导入QT-Design生成的UI
from ui.login_ui import Ui_Form
from ui.registe_ui import Ui_Dialog

# 导入设计好的检测界面
from Detect_GUI import Ui_MainWindow

# 界面登录
class win_Login(QMainWindow):
    def __init__(self, parent = None):
        super(win_Login, self).__init__(parent)
        self.ui_login = Ui_Form()
        self.ui_login.setupUi(self)
        self.init_slots()
        self.hidden_pwd()

    # 密码输入框隐藏
    def hidden_pwd(self):
        self.ui_login.edit_password.setEchoMode(QLineEdit.Password)

    # 绑定信号槽
    def init_slots(self):
        self.ui_login.btn_login.clicked.connect(self.onSignIn) # 点击按钮登录
        self.ui_login.edit_password.returnPressed.connect(self.onSignIn) # 按下回车登录
        self.ui_login.btn_regeist.clicked.connect(self.create_id)

    # 跳转到注册界面
    def create_id(self):
        shareInfo.createWin = win_Registe()
        shareInfo.createWin.show()

    # 保存登录日志
    def sava_login_log(self, username):
        with open('login_log.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\t log in at' + datetime.now().strftimestrftime+ '\r')

    # 登录
    def onSignIn(self):
        print("You pressed sign in")
        # 从登陆界面获得输入账户名与密码
        username = self.ui_login.edit_username.text().strip()
        password = self.ui_login.edit_password.text().strip()
        print(username)
        print(password)
        # 获得账号信息
        USER_PWD = get_id_info()
        # print(USER_PWD)
        if username not in USER_PWD.keys():
            replay = QMessageBox.warning(self,"登陆失败!", "账号或密码输入错误", QMessageBox.Yes)
        else:
            # 若登陆成功，则跳转主界面
            if USER_PWD.get(username) == password:
                print("Jump to main window")
                # 所以使用公用变量名
                shareInfo.createWin = Ui_MainWindow()
                shareInfo.createWin.show()
                # 关闭当前窗口
                self.close()
            else:
                replay = QMessageBox.warning(self, "!", "账号或密码输入错误", QMessageBox.Yes)

# 注册界面
class win_Registe(QMainWindow):
    def __init__(self, parent = None):
        super(win_Registe, self).__init__(parent)
        self.ui_registe = Ui_Dialog()
        self.ui_registe.setupUi(self)
        self.init_slots()

    # 绑定槽信号
    def init_slots(self):
        self.ui_registe.pushButton_regiser.clicked.connect(self.new_account)
        self.ui_registe.pushButton_cancer.clicked.connect(self.cancel)

    # 创建新账户
    def new_account(self):
        print("Create new account")
        USER_PWD = get_id_info()
        # print(USER_PWD)
        new_username = self.ui_registe.edit_username.text().strip()
        new_password = self.ui_registe.edit_password.text().strip()
        # 判断用户名是否为空
        if new_username == "":
            replay = QMessageBox.warning(self, "!", "账号不准为空", QMessageBox.Yes)
        else:
            # 判断账号是否存在
            if new_username in USER_PWD.keys():
                replay = QMessageBox.warning(self, "!", "账号已存在", QMessageBox.Yes)
            else:
                # 判断密码是否为空
                if new_password == "":
                    replay = QMessageBox.warning(self, "!", "密码不能为空", QMessageBox.Yes)
                else:
                    # 注册成功
                    print("Successful!")
                    sava_id_info(new_username, new_password)
                    replay = QMessageBox.warning(self,  "!", "注册成功！", QMessageBox.Yes)
                    # 关闭界面
                    self.close()

    # 取消注册
    def cancel(self):
        self.close() # 关闭当前界面

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('ui_img/icon.png'))
    # 利用共享变量名来实例化对象
    shareInfo.loginWin = win_Login() # 登录界面作为主界面
    shareInfo.loginWin.show()
    sys.exit(app.exec_())

