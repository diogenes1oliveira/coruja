#!/usr/bin/env python3

import importlib
import unittest

import psutil

from coruja import windowinspector


class ProcessMock:
    def __init__(self, pid):
        self.pid = pid

        if pid == 10:
            self._name = 'myprocess10'
        elif pid == 222:
            self._name = 'myprocess222'
        else:
            raise psutil.NoSuchProcess(pid)

    def name(self):
        return self._name


class TestWindow(unittest.TestCase):
    def setUp(self):
        psutil.Process = ProcessMock

    def tearDown(self):
        importlib.reload(psutil)

    def test_init(self):
        w = windowinspector.Window(11, 'any name', 222)
        self.assertEqual(w.wid, 11)
        self.assertEqual(w.title, 'any name')
        self.assertEqual(w.pid, 222)

    def test_cmp(self):
        self.assertLess(windowinspector.Window(33, 'Title', 10),
                        windowinspector.Window(333, 'Title', 222))
        self.assertLess(windowinspector.Window(33, 'Title2', 10),
                        windowinspector.Window(333, 'Title3', 10))
        w1 = windowinspector.Window(244, 'Title30', 222)
        w2 = windowinspector.Window(244, 'arbitrary Title', 10)
        self.assertEqual(w1, w2, str((w1, w2)))

    def test_process_name(self):
        w10 = windowinspector.Window(00, '', pid=10)
        self.assertEqual(w10.process_name, 'myprocess10', w10)

        w222 = windowinspector.Window(00, '', pid=222)
        self.assertEqual(w222.process_name, 'myprocess222', w222)

        w333 = windowinspector.Window(00, '', pid=333)
        self.assertEqual(w333.process_name, '', w333)
