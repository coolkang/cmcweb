# -*- coding: utf-8 -*-
import struct
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Float
from sqlalchemy import desc
from urllib import quote_plus as urlquote


db_engine = create_engine("mysql+pymysql://root:%s@localhost/cmcweb" % urlquote("nimd@123!"))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Ip2Location(Base):
    __tablename__ = "ip2location_db5"
    ip_from = Column(BigInteger, primary_key=True)
    ip_to = Column(BigInteger, primary_key=True)
    country_code = Column(String)
    country_name = Column(String)
    region_name = Column(String)
    city_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)


def _parse_addr(addr):
    ''' Parses address and returns IP version. Raises exception on invalid argument '''
    ipv = 0
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        # Convert ::FFFF:x.y.z.y to IPv4
        if addr.lower().startswith('::ffff:'):
            try:
                socket.inet_pton(socket.AF_INET, addr)
                ipv = 4
            except:
                ipv = 6
        else:
            ipv = 6
    except:
        socket.inet_pton(socket.AF_INET, addr)
        ipv = 4
    return ipv


def inet_pton(ip):
    ipv = _parse_addr(ip)

    if ipv == 4:
        ipno = struct.unpack('!L', socket.inet_pton(socket.AF_INET, ip))[0]
    elif ipv == 6:
        a, b = struct.unpack('!QQ', socket.inet_pton(socket.AF_INET6, ip))
        ipno = (a << 64) | b

    return ipno


def get_info(ip_addr):
    ip_pton = inet_pton(ip_addr)

    return db_session.query(Ip2Location).filter(Ip2Location.ip_from <= ip_pton).order_by(desc(Ip2Location.ip_from)).limit(1).first()


def get_degraded_ip():
    return db_session.execute("select webpages_accesslocation.id, webpages_useraccess.ip_addr from webpages_accesslocation join webpages_useraccess on webpages_accesslocation.access_id_id = webpages_useraccess.id where city is null limit 1000;")


if __name__ == "__main__":
    degraded_ip_list = get_degraded_ip()

    count = 0
    for ip in degraded_ip_list:
        useraccess_id = ip[0]
        ip_addr = ip[1]
        loc_info = get_info(ip_addr)
        print(loc_info.city_name)

        try:
            db_session.execute("update webpages_accesslocation set city = '{0}', lat = {1}, lon = {2} where id = {3}".format(loc_info.city_name, loc_info.latitude, loc_info.longitude, useraccess_id))
            count += 1
        except:
            pass

    db_session.commit()
    print("{0} rows updated".format(count))
