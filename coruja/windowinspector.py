#!/bin/bash

import psutil


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


class WindowInspector:
    def __init__(self, on_activate):
        pass

    def get_active_windows(self):
        pass

    def get_active_window(self):
        pass
