import pytest
import ipintellib
import random


def test_getVersion():
    version = ipintellib.getVersion()
    assert version == "1.10"


def test_getDatabase():
    database_location = ipintellib.getDatabase()
    assert database_location == "/usr/local/share/GeoIP/GeoLiteCity.dat"

@pytest.mark.parametrize("ip, countryCode, countryName, city",
                          [
                              ("1.2.3.4", "AU", "Australia", 'None'),
                              ("8.8.8.8", "US", "United States", 'Mountain View'),
                              ("88.109.78.193", "GB", "United Kingdom", 'Hornchurch'),
                          ]
                          )
def test_geo_ip(ip, countryCode, countryName, city):
    ip_info = ipintellib.geo_ip(ip)
    assert ip_info['countryCode'] == countryCode
    assert ip_info['countryName'] == countryName
    assert ip_info['city'] == city


def test_geo_ip_random():
    for i in range(0, 9889):
        first = int(255 * random.random())
        second = int(255 * random.random())
        third = int(255 * random.random())
        fourth = int(255 * random.random())
        random_ip = first.__str__() + '.' + second.__str__() + '.' + third.__str__() + '.' + fourth.__str__()
        ip_info = ipintellib.geo_ip(random_ip)


def test_geo_ip_bad_1():
    ip_info = ipintellib.geo_ip("0.0.0.0.0.0.0")
    assert ip_info['city'] == 'None'
