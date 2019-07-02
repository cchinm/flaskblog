import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'iwinter@aliyun.com'
receivers = ['chinming95@sohu.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
def sendmail(name, msg, mail):
    html = """
    你好，%s 先生/女士：
        我已收到你关于   %s 的问题反馈。我们将及时处理。
        如还有其他问题，可联系邮箱 iwinter@aliyun.com
     
    """ % (name, msg)
    print(html)
    message = MIMEText(html, "html","utf-8")
    message['From'] = Header("iwinter@aliyun.com", 'utf-8')  # 发送者
    message['To'] = Header(mail, 'utf-8')  # 接收者

    subject = 'CrazyBlog疯部落-反馈回复'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # smtp = smtplib.SMTP("smtp.aliyun.com", )
        smtp = smtplib.SMTP_SSL("smtp.aliyun.com", 465)
        smtp.set_debuglevel(0)
        smtp.ehlo()
        # smtp.login("chinming95@sohu.com", "z136789")
        smtp.login("iwinter@aliyun.com", "zm119162")
        smtp.sendmail("iwinter@aliyun.com",
                      [mail,],
                      message.as_string())
        smtp.close()


        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


# sendmail("ming","hao","chinming95@sohu.com")