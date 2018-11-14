from random import Random
from django.core.mail import send_mail

from mxonline_chen.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def random_str(len_random=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(len_random):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: <a href='http://127.0.0.1:8000/active/{0}' /a>".format(code)
        send_status = send_mail(subject=email_title, message="", from_email=EMAIL_FROM, recipient_list=[email, ],html_message=email_body)
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的链接重置你的密码: <a href='http://127.0.0.1:8000/reset/{0}' /a>".format(code)
        send_status = send_mail(subject=email_title, message="", from_email=EMAIL_FROM, recipient_list=[email, ],
                                html_message=email_body)
        if send_status:
            pass
