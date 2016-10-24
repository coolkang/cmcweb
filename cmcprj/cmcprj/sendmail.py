# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email import Utils
from email.header import Header
import os

from settings.mail_list import mail_list
import pymysql


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='btj1040!', db='cmcweb')
cur = conn.cursor()


# smtp_server  = "smtp 서버"
# port = smtp 포트번호
# userid = "smtp 접속 아이디"
# passwd = "smtp 비밀번호"

def send_mail(from_user, to_user, cc_users, subject, text, attach):
        COMMASPACE = ", "
        msg = MIMEMultipart("alternative")
        msg["From"] = from_user
        msg["To"] = to_user
        msg["Cc"] = COMMASPACE.join(cc_users)
        msg["Subject"] = Header(s=subject, charset="utf-8")
        msg["Date"] = Utils.formatdate(localtime=1)
        msg.attach(MIMEText(text, "html", _charset="utf-8"))

        if (attach is not None):
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(attach, "rb").read())
                Encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % os.path.basename(attach))
                msg.attach(part)

        smtp = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        smtp.login("info@hadiye.org", "J2$us.L0rd!")
        smtp.sendmail(from_user, cc_users, msg.as_string())
        smtp.close()


if __name__ == "__main__":
    for to_user, countries in mail_list:
        for country in countries:
            cur.execute("select count(*) from webpages_useraccess ua join webpages_accesslocation al on ua.id = al.access_id_id where al.country = '{0}' and ua.timestamp > date_sub(curdate(), interval 30 day)".format(country))
            total_count = 0
            for row in cur:
                total_count = row[0]

            cur.execute("select count(*) from webpages_useraccess ua join webpages_accesslocation al on ua.id = al.access_id_id where al.country = '{0}' and ua.accepted = 'yes' and ua.timestamp > date_sub(curdate(), interval 30 day)".format(country))
            accepted_count = 0
            for row in cur:
                accepted_count = row[0]

            emails = []
            cur.execute("select distinct(ua.email) from webpages_useraccess ua join webpages_accesslocation al on ua.id = al.access_id_id where al.country = '{0}' and ua.timestamp > date_sub(curdate(), interval 30 day)".format(country))
            for row in cur:
                if row[0] is not None:
                    emails.append(row[0])

            msg_body = """
                Stats for last 30 days<br/>
                total accesses: {0}<br/>
                gospel accepted: {1}<br/>
                <br/>
                Contacts remained<br/>
                {2}
            """.format(total_count, accepted_count, "<br/>".join(emails))

            send_mail("info@hadiye.org", to_user, [to_user], "Gospel Media Campaign Report for {0}".format(country), msg_body, None)

    cur.close()
    conn.close()
