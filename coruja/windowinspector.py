#!/bin/bash

import logging
import psutil
import gi.repository.Wnck as Wnck
import gi.repository.Gtk as Gtk
import gi.repository.GObject as GObject


class Window:
    def __init__(self, wid, title, pid):
        self.wid = wid
        self.title = title
        self.pid = pid

    @property
    def process_name(self):
        try:
            return psutil.Process(self.pid).name()
        except psutil.NoSuchProcess:
            return ''

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'Window(wid={}, title={}, pid={})'.format(self.wid, self.title, self.pid)

    def __lt__(self, other):
        return self.wid < other.wid

    def __eq__(self, other):
        return self.wid == other.wid

    def __hash__(self):
        return hash(self.wid)


class WindowInspector(GObject.GObject):
    def __init__(self, on_activate):
        GObject.GObject.__init__(self)
        self.on_activate = on_activate

        screen = Wnck.Screen.get_default()
        screen.connect('active-window-changed', self._process_window_change)

    def _process_window_change(self, screen, win0):
        w = screen.get_active_window()
        if w is None:
            return

        win = Window(w.get_xid(), w.get_name(), w.get_pid())
        logging.debug('Active window changed to %s', win)
        self.on_activate(win)

    def quit(self):
        Gtk.main_quit()

    def get_active_windows(self):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        return [Window(w.get_xid(), w.get_name(), w.get_pid())
                for w in screen.get_windows()]

    def get_active_window(self):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        w = screen.get_active_window()
        if w is None:
            logging.debug("screen.get_active_window() returned None")
        return Window(w.get_xid(), w.get_name(), w.get_pid())

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    logging.basicConfig(level=logging.DEBUG)
    Gtk.init([])
    inspector = WindowInspector(lambda w: print("MUDOU %s"%w))
    Gtk.main()