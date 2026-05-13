#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject

import os
import socket
import subprocess
import locale
from locale import gettext as _

locale.bindtextdomain('pardus-finance', '/usr/share/locale')
locale.textdomain('pardus-finance')

GLADE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/MainWindow.glade")


class pardusfinance:
    def __init__(self):
        self.flask_process = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)

        # widget referances
        self.window = self.builder.get_object("mainwindow")  # home window
        self.window.set_decorated(False)  # remove window decoration

        self.cssload()  # CSS desing

        self.window.set_keep_above(True)  # always keep it on top

        # signals
        self.window.connect("realize", self.on_realize)  # when realized, the Gdk.Window file belonging to the window will be ready
        self.window.connect("destroy", self._on_destroy)
        self.window.show_all()


    # CSS theme
    def cssload(self):
        css = b"""

        window { background-color: rgba(10, 10, 10, 10); border-radius: 15px; }

        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    # window resizer and router
    def on_realize(self, win):
        screen = win.get_screen()
        monitor = screen.get_primary_monitor()
        geom = screen.get_monitor_geometry(monitor)

        width, height = win.get_size()
        # move to bottom right corner (padding 10px)
        x = geom.x + geom.width - width - 10
        y = geom.y + geom.height - height - 10
        win.move(x, y)

    def _on_destroy(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    app = pardusfinance()
    Gtk.main()

