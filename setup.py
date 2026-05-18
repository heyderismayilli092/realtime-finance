#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup, find_packages


def create_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir, po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(podir, po.split(".po")[0], "pardus-finance.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["po/" + po.split(".po")[0] + "/LC_MESSAGES/pardus-finance.mo"]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.1"
    f = open("src/__version__", "w")
    f.write(version)
    f.close()

data_files = [
    ("/usr/bin", ["pardus-finance"]),

    ("/usr/share/applications",
     ["tr.org.pardus.finance.desktop"]),

    ("/usr/share/pardus/pardus-finance/ui",
     ["ui/MainWindow.glade"]),

    ("/usr/share/pardus/pardus-finance/src", ["src/main.py"]),

    ("/usr/lib/python3/dist-packages/", ["src/kur_api.py"]),

    ("/usr/share/icons/hicolor/scalable/apps/",
     ["pardus-finance.png"])
] + create_mo_files()

setup(
    name="pardus-finance",
    version=version,
    packages=find_packages(),
    scripts=["pardus-finance"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Heydar Ismayilli",
    author_email="heyderismayilli092@gmail.com",
    description="A simple application that displays currency and gold exchange rate changes on the Pardus desktop screen",
    license="GPLv3",
    keywords="pardus-finance, finance, dollar, euro, gold",
    url="https://github.com/heyderismayilli092/pardus-finance",
)

