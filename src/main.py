#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib

import os
import socket
import subprocess
import locale
from locale import gettext as _

locale.bindtextdomain('pardus-finance', '/usr/share/locale')
locale.textdomain('pardus-finance')

GLADE_FILE = os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade"


class pardusfinance:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)

        # widget referances
        self.window = self.builder.get_object("mainwindow")  # home window
        self.update_time_label = self.builder.get_object("update_time")
        self.close_button = self.builder.get_object("closebutton")  # close button

        # transparency window
        self.window.set_decorated(False)  # remove window decoration
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.window.set_visual(visual)
        self.window.set_keep_above(True)  # always keep it on top

        # signals
        self.window.connect("realize", self.on_realize)  # when realized, the Gdk.Window file belonging to the window will be ready
        self.window.connect("destroy", self._quit)
        self.close_button.connect("clicked", self._quit)
        self.count = 0
        GLib.timeout_add_seconds(2, self._tick)  # '_tick' fonksiyonu her defasında 3 saniyeden bir çalışır
        self.window.show_all()
        self.cssload()  # CSS desing


    # CSS theme
    def cssload(self):
        css = b"""
        window { background-color: rgba(80, 83, 84, 0.4); border-radius: 20px; color: #fff; }
        button {
            background-image: none;
            background-color: #d64a4a;
            color: #fff;
            border-radius: 10px;
        }
        button:hover {
          background-color: #560000;
        }
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

    # finance API function
    def _tick(self):
        self.count += 1
        self.update_time_label.set_text(str(self.count))
        return True

    # quit
    def _quit(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    app = pardusfinance()
    Gtk.main()

