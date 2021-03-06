"""
Copyright (C) 2018 IAIK TU Graz (data@iaik.tugraz.at)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

@version 1.2

"""

from PyQt5.Qsci import QsciScintilla, QsciLexerCPP
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import QTabWidget, QFrame

from datagui.package.utils import LeakFlags, getIconById, debug, default_font_size

class ZoomTabView(QTabWidget):

    def __init__(self):
        super(ZoomTabView, self).__init__()
        self.zoomlevel = 0
        self.zoomlevel_min = -10
        self.zoomlevel_max = 30

    def scaleAllTabs(self, increment = 0):
        self.zoomlevel = int(self.zoomlevel + increment)
        if self.zoomlevel < self.zoomlevel_min:
            self.zoomlevel = self.zoomlevel_min
        elif self.zoomlevel > self.zoomlevel_max:
            self.zoomlevel = self.zoomlevel_max
        self.syncTabScalingToZoomlevel()

    def syncTabScalingToZoomlevel(self):
        current = self.currentIndex()
        for i in range(self.count() - 1):
            editor = self.widget(i)
            # SCI_SETZOOM doesn't seem to work properly for negative numbers,
            # so we use SCI_ZOOMIN/SCI_ZOOMOUT.
            while editor.SendScintilla(QsciScintilla.SCI_GETZOOM) > self.zoomlevel:
                editor.SendScintilla(QsciScintilla.SCI_ZOOMOUT)
            while editor.SendScintilla(QsciScintilla.SCI_GETZOOM) < self.zoomlevel:
                editor.SendScintilla(QsciScintilla.SCI_ZOOMIN)
            self.recomputeMarkers(editor)

    def wheelEvent(self, qwheelevent):
        if self.currentIndex() == self.count() - 1:
            # Don't scroll on No-File tab
            return
        self.zoomlevel = self.currentWidget().SendScintilla(QsciScintilla.SCI_GETZOOM)
        self.syncTabScalingToZoomlevel()
