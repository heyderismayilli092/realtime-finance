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
import kur_api  # the code that retrieves currency data is being imported

locale.bindtextdomain('realtime-finance', '/usr/share/locale')
locale.textdomain('realtime-finance')

GLADE_FILE = os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade"


class realtimefinance:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)

        # widget referances
        self.window = self.builder.get_object("mainwindow")  # home window
        self.about_dialog = self.builder.get_object("about_dialog")  # about screen
        self.connection = self.builder.get_object("connection")

        self.close_button = self.builder.get_object("closebtn")  # close button
        self.close_button.set_name("closebtn")  # for CSS
        self.about_button = self.builder.get_object("aboutbtn")  # about button
        self.about_button.set_name("aboutbtn")  # for CSS

        self.usdalis = self.builder.get_object("usd_alis")  # usd_alis label
        self.usdsatis = self.builder.get_object("usd_satis")  # usd_satis label
        self.usddegisim = self.builder.get_object("usd_degisim")  # usd_degisim label

        self.euroalis = self.builder.get_object("euro_alis")  # euro_alis label
        self.eurosatis = self.builder.get_object("euro_satis")  # euro_satis label
        self.eurodegisim = self.builder.get_object("euro_degisim")  # euro_degisim label

        self.caalis = self.builder.get_object("ca_alis")  # ca_alis label
        self.casatis = self.builder.get_object("ca_satis")  # ca_satis label
        self.cadegisim = self.builder.get_object("ca_degisim")  # ca_degisim label

        self.gaalis = self.builder.get_object("ga_alis")  # ga_alis label
        self.gasatis = self.builder.get_object("ga_satis")  # ga_satis label
        self.gadegisim = self.builder.get_object("ga_degisim")  # ga_degisim label

        # stack properties
        self.stack = self.builder.get_object("main_stack")
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.stack.set_transition_duration(1000)  # ms

        self.page_index = 5
        self.pages = ["page0", "page1", "page2", "page3"]  # pages displaying exchange rate data

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
        self.about_button.connect("clicked", self._on_aboutdialog)

        self.current = 0
        self.refresh_data()  # the exchange rate data should be obtained when the program first starts

        GLib.timeout_add_seconds(5, self.boxchange)  # 'boxchange' fonksiyonu her defasında 5 saniyeden bir çalışır
        self.window.show_all()
        self.cssload()  # CSS desing


    # CSS theme
    def cssload(self):
        css = b"""

        window { background-color: rgba(80, 83, 100, 0.7); border-radius: 20px; color: #fff; }
        #closebtn {
            background-image: none;
            background-color: #d64a4a;
            color: #fff;
            border-radius: 10px;
            opacity: 0.5;
        }
        #closebtn:hover {
          background-color: #560000;
        }

        #aboutbtn {
            opacity: 0.5;
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


    # new market data is retrieved and printed to the appropriate objects
    def refresh_data(self):
        kurdata = kur_api.kur()
        # if it returns 1, it indicates that there is no internet connection; if it returns 2, it indicates that the connection timed out
        if kurdata == 1:
          return 1
        elif kurdata == 2:
          return 2

        self.usdalis.set_label(kurdata['usd']['alis'])
        self.usdsatis.set_label(kurdata['usd']['satis'])
        # the colors are displayed according to the exchange rate
        if kurdata['usd']['degisim'][0:1] == "-":
          markup = "<span foreground='#ff0000'>{val}</span>".format(val=kurdata['usd']['degisim'])
          self.usddegisim.set_markup(markup)
        elif kurdata['usd']['degisim'][0:1] == "+":
          markup = "<span foreground='#12ff34'>{val}</span>".format(val=kurdata['usd']['degisim'])
          self.usddegisim.set_markup(markup)

        self.euroalis.set_label(kurdata['eur']['alis'])
        self.eurosatis.set_label(kurdata['eur']['satis'])
        # the colors are displayed according to the exchange rate
        if kurdata['eur']['degisim'][0:1] == "-":
          markup = "<span foreground='#ff0000'>{val}</span>".format(val=kurdata['eur']['degisim'])
          self.eurodegisim.set_markup(markup)
        elif kurdata['eur']['degisim'][0:1] == "+":
          markup = "<span foreground='#12ff34'>{val}</span>".format(val=kurdata['eur']['degisim'])
          self.eurodegisim.set_markup(markup)

        self.gaalis.set_label(kurdata['ga']['alis'])
        self.gasatis.set_label(kurdata['ga']['satis'])
        # the colors are displayed according to the exchange rate
        if kurdata['ga']['degisim'][0:1] == "-":
          markup = "<span foreground='#ff0000'>{val}</span>".format(val=kurdata['ga']['degisim'])
          self.gadegisim.set_markup(markup)
        elif kurdata['ga']['degisim'][0:1] == "+":
          markup = "<span foreground='#12ff34'>{val}</span>".format(val=kurdata['ga']['degisim'])
          self.gadegisim.set_markup(markup)

        self.caalis.set_label(kurdata['ca']['alis'])
        self.casatis.set_label(kurdata['ca']['satis'])
        # the colors are displayed according to the exchange rate
        if kurdata['ca']['degisim'][0:1] == "-":
          markup = "<span foreground='#ff0000'>{val}</span>".format(val=kurdata['ca']['degisim'])
          self.cadegisim.set_markup(markup)
        elif kurdata['ca']['degisim'][0:1] == "+":
          markup = "<span foreground='#12ff34'>{val}</span>".format(val=kurdata['ca']['degisim'])
          self.cadegisim.set_markup(markup)


    # data box change
    def boxchange(self):
        if self.page_index >= len(self.pages):
            self.page_index = 0
            output = self.refresh_data()  # the API is called again
            # connection checking flow:
            # data from the refresh_data() function is received and checked. If it returns 1, it indicates that there is no internet connection; if it returns 2, it indicates that the connection timed out
            # if either of these error codes is received, the appropriate error message is displayed
            if output == 1:
              self.connection.set_label(_("Could not connect to the API service.\nPlease check your internet connection"))
              self.stack.set_visible_child_name("page4")
              return False
            elif output == 2:
              self.connection.set_label(_("The connection timed out.\nPlease close and reopen the app to try again"))
              self.stack.set_visible_child_name("page4")
              return False

        # next index
        self.current = (self.current + 1) % len(self.pages)
        name = self.pages[self.current]
        # change the visible box
        self.stack.set_visible_child_name(name)

        self.page_index += 1
        return True


    # about dialog
    def _on_aboutdialog(self, widget):
        self.about_dialog.run()
        self.about_dialog.hide()


    # quit
    def _quit(self, widget):
        Gtk.main_quit()



app = realtimefinance()
Gtk.main()

