from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class Email_163:
    def __init__(self, text):
        self.from_addr = 'freefh@yeah.net'  # 发送地址
        self.password = 'MXKMUAZEGWACWKOQ'  # 验证
        self.to_addr = '2410772045@qq.com'  # 发送到
        self.smtp_server = 'smtp.yeah.net'  # 服务器地址
        self.text = text

    def _format_addr(self, s):  # 格式化字符串
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def setting(self):
        self.msg = MIMEText(_text=self.text, _charset='utf-8')
        self.msg['From'] = self._format_addr('二号爬虫<%s>' % self.from_addr)
        self.msg['To'] = self._format_addr('管理员<%s>' % self.to_addr)
        self.msg['Subject'] = Header('一号爬虫运行状态', 'utf-8').encode()

    def send(self):
        server = smtplib.SMTP(self.smtp_server, 25)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        server.quit()

    def run(self):
        self.setting()
        self.send()
        print("发送成功！")


if __name__ == "__main__":
    send = Email_163('我还没吃饭呢，想吃饭了！')
    send.run()
