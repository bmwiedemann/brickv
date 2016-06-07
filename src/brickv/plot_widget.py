# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014, 2016 Matthias Bolte <matthias@tinkerforge.com>

plot_widget.py: Graph for simple value over time representation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys
import math
import functools
import bisect

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QWidget, QToolButton, \
                        QPainter, QSizePolicy, QFontMetrics, QPixmap, \
                        QIcon, QColor, QCursor, QPen, QPainterPath, QLabel, \
                        QTransform, QPalette
from PyQt4.QtCore import QTimer, Qt, QSize, QPointF, QRectF, QLineF

EPSILON = 0.000001
DEBUG = False

def istr(i):
    return str(int(i))

def fstr(f):
    s = ('%.10f' % f).rstrip('0')

    if s.endswith('.'):
        s += '0'

    return s

def fuzzy_eq(a, b):
    return abs(a - b) < EPSILON

def fuzzy_leq(a, b):
    return a < b or fuzzy_eq(a, b)

def fuzzy_geq(a, b):
    return a > b or fuzzy_eq(a, b)

class Scale(object):
    def __init__(self, tick_text_font, title_text_font):
        self.axis_line_thickness = 1 # px, fixed

        self.tick_mark_thickness = 1 # px, fixed
        self.tick_mark_size_small = 5 # px, fixed
        self.tick_mark_size_medium = 7 # px, fixed
        self.tick_mark_size_large = 9 # px, fixed

        self.tick_text_font = tick_text_font
        self.tick_text_font_metrics = QFontMetrics(self.tick_text_font)
        self.tick_text_height = self.tick_text_font_metrics.boundingRect('0123456789').height()
        self.tick_text_height_half = int(math.ceil(self.tick_text_height / 2.0))

        self.tick_value_to_str = istr

        self.title_text_font = title_text_font
        self.title_text_font_metrics = QFontMetrics(self.title_text_font)

class XScale(Scale):
    def __init__(self, tick_text_font, title_text_font, title_text):
        Scale.__init__(self, tick_text_font, title_text_font)

        self.tick_mark_to_tick_text = 0 # px, fixed

        self.tick_text_to_title_text = 4 # px, fixed

        self.title_text = title_text
        self.title_text_height = self.title_text_font_metrics.boundingRect(self.title_text).height()
        self.title_text_to_border = 2 # px, fixed

        self.total_height = self.axis_line_thickness + \
                            self.tick_mark_size_large + \
                            self.tick_mark_to_tick_text + \
                            self.tick_text_height + \
                            self.tick_text_to_title_text + \
                            self.title_text_height + \
                            self.title_text_to_border # px, fixed

    def draw(self, painter, factor, tick_value_min, tick_count):
        factor_int = int(math.floor(factor))
        text_flags = Qt.TextDontClip | Qt.AlignHCenter | Qt.AlignBottom

        # axis line
        axis_line_length = int(math.floor(factor * tick_count))

        painter.drawLine(0, 0, axis_line_length - 1, 0)

        # ticks
        tick_text_y = self.axis_line_thickness + \
                      self.tick_mark_size_large + \
                      self.tick_mark_to_tick_text
        tick_text_width = factor_int + self.tick_mark_thickness + factor_int
        tick_text_height = self.tick_text_height

        painter.setFont(self.tick_text_font)

        for i in range(tick_count):
            x = round(factor * i)
            tick_value = int(tick_value_min + i)

            if (tick_value % 5) == 0:
                tick_mark_size = self.tick_mark_size_large
                tick_text_x = x - factor_int

                if DEBUG:
                    painter.fillRect(tick_text_x, tick_text_y,
                                     tick_text_width, tick_text_height,
                                     Qt.yellow)

                painter.drawText(tick_text_x, tick_text_y,
                                 tick_text_width, tick_text_height,
                                 text_flags,
                                 self.tick_value_to_str(tick_value))
            else:
                tick_mark_size = self.tick_mark_size_small

            painter.drawLine(x, 0, x, tick_mark_size)

        # title
        title_text_x = 0
        title_text_y = self.axis_line_thickness + \
                       self.tick_mark_size_large + \
                       self.tick_mark_to_tick_text + \
                       self.tick_text_height + \
                       self.tick_text_to_title_text
        title_text_width = axis_line_length
        title_text_height = self.title_text_height

        if DEBUG:
            painter.fillRect(title_text_x, title_text_y,
                             title_text_width, title_text_height,
                             Qt.yellow)

        painter.setFont(self.title_text_font)
        painter.drawText(title_text_x, title_text_y,
                         title_text_width, title_text_height,
                         text_flags, self.title_text)

class YScale(Scale):
    def __init__(self, tick_text_font, title_text_font, title_text):
        Scale.__init__(self, tick_text_font, title_text_font)

        self.value_min = None # set by update_tick_config
        self.value_max = None # set by update_tick_config

        self.step_size = None # set by update_tick_config
        self.step_subdivision_count = None # set by update_tick_config

        self.tick_mark_to_tick_text = 3 # px, fixed

        self.tick_text_to_title_text = 7 # px, fixed
        self.tick_text_max_width = 10 # px, initial value, calculated in update_tick_config

        self.title_text = title_text
        self.title_text_to_border = 2 # px, fixed
        self.title_text_height = None # set by update_title_text_height
        self.title_text_pixmap = None

        self.total_width = None # set by update_total_width
        self.total_width_changed = None

        self.update_title_text_height(1000)
        self.update_tick_config(-1.0, 1.0, 1.0, 5)

    def update_tick_config(self, value_min, value_max, step_size, step_subdivision_count):
        self.value_min = value_min
        self.value_max = value_max
        self.step_size = step_size
        self.step_subdivision_count = step_subdivision_count

        if fuzzy_geq(self.step_size, 1.0):
            self.tick_value_to_str = istr
        else:
            self.tick_value_to_str = fstr

        value = self.value_min
        tick_text_max_width = self.tick_text_font_metrics.width(self.tick_value_to_str(value))

        while fuzzy_leq(value, self.value_max):
            tick_text_max_width = max(tick_text_max_width, self.tick_text_font_metrics.width(self.tick_value_to_str(value)))
            value += self.step_size

        self.tick_text_max_width = tick_text_max_width

        self.update_total_width()

    def update_title_text_height(self, max_width):
        self.title_text_height = self.title_text_font_metrics.boundingRect(0, 0, max_width, 1000,
                                                                           Qt.TextWordWrap | Qt.AlignHCenter | Qt.AlignTop,
                                                                           self.title_text).height()

        self.update_total_width()

    def update_total_width(self):
        old_total_width = self.total_width

        self.total_width = self.axis_line_thickness + \
                           self.tick_mark_size_large + \
                           self.tick_mark_to_tick_text + \
                           self.tick_text_max_width + \
                           self.tick_text_to_title_text + \
                           self.title_text_height + \
                           self.title_text_to_border

        if old_total_width != self.total_width and self.total_width_changed != None:
            self.total_width_changed()

    def draw(self, painter, height, factor):
        # axis line
        painter.drawLine(-self.axis_line_thickness, 0, -self.axis_line_thickness, -height + 1)

        # ticks
        painter.setFont(self.tick_text_font)

        tick_text_x = -self.axis_line_thickness - \
                      self.tick_mark_size_large - \
                      self.tick_mark_to_tick_text - \
                      self.tick_text_max_width
        tick_text_width = self.tick_text_max_width
        tick_text_height = self.tick_text_height_half * 2

        value = self.value_min

        while fuzzy_leq(value, self.value_max):
            y = -int(round((value - self.value_min) * factor))

            painter.drawLine(-self.axis_line_thickness, y,
                             -self.axis_line_thickness - self.tick_mark_size_large, y)

            tick_text_y = y - self.tick_text_height_half

            if DEBUG:
                painter.fillRect(tick_text_x, tick_text_y,
                                 tick_text_width, tick_text_height,
                                 Qt.yellow)

            painter.drawText(tick_text_x, tick_text_y, tick_text_width, tick_text_height,
                             Qt.TextDontClip | Qt.AlignRight | Qt.AlignVCenter,
                             self.tick_value_to_str(value))

            for i in range(1, self.step_subdivision_count):
                subvalue = value + (self.step_size * i / self.step_subdivision_count)

                if not fuzzy_leq(subvalue, self.value_max):
                    break

                suby = -int(round((subvalue - self.value_min) * factor))

                if i % 2 == 0 and self.step_subdivision_count % 2 == 0:
                    tick_mark_size = self.tick_mark_size_medium
                else:
                    tick_mark_size = self.tick_mark_size_small

                painter.drawLine(-self.axis_line_thickness, suby,
                                 -self.axis_line_thickness - tick_mark_size, suby)

            value += self.step_size

        # title
        title_width = height
        title_height = self.title_text_height

        if self.title_text_pixmap == None or self.title_text_pixmap.size() != QSize(title_width, title_height):
            self.title_text_pixmap = QPixmap(title_width, title_height)

            if DEBUG:
                self.title_text_pixmap.fill(Qt.yellow)
            else:
                self.title_text_pixmap.fill(QColor(0, 0, 0, 0))

            title_painter = QPainter(self.title_text_pixmap)
            title_painter.setFont(self.title_text_font)
            title_painter.drawText(0, 0, title_width, title_height,
                                  Qt.TextWordWrap | Qt.TextDontClip | Qt.AlignHCenter | Qt.AlignTop,
                                  self.title_text)
            title_painter = None

        painter.save()
        painter.rotate(-90)

        title_x = -1
        title_y = -self.axis_line_thickness - \
                  self.tick_mark_size_large - \
                  self.tick_mark_to_tick_text - \
                  self.tick_text_max_width - \
                  self.tick_text_to_title_text - \
                  title_height

        painter.drawPixmap(title_x, title_y, self.title_text_pixmap)

        painter.restore()

class CurveArea(QWidget):
    def __init__(self, plot):
        QWidget.__init__(self, plot)

        self.plot = plot

        # FIXME: need to enable opaque painting to avoid that updates of other
        #        widgets trigger a full update of the curve
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)

    # override QWidget.paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        if DEBUG:
            painter.fillRect(0, 0, width, height, Qt.blue)
        else:
            painter.fillRect(event.rect(), self.plot.canvas_color)

        y_min_scale = self.plot.y_scale.value_min
        y_max_scale = self.plot.y_scale.value_max

        factor_x = float(width) / self.plot.history_length_x
        factor_y = float(height - 1) / max(y_max_scale - y_min_scale, EPSILON) # -1 to accommodate the 1px width of the curve

        if self.plot.x_min != None and self.plot.x_max != None:
            x_min = self.plot.x_min
            x_max = self.plot.x_max

            if self.plot.scales_visible:
                curve_x_offset = 0
            else:
                curve_x_offset = round((self.plot.history_length_x - (x_max - x_min)) * factor_x)

            transform = QTransform()

            transform.translate(curve_x_offset,
                                height - 1 + self.plot.curve_y_offset) # -1 to accommodate the 1px width of the curve
            transform.scale(factor_x, -factor_y)
            transform.translate(-x_min, -y_min_scale)

            self.plot.partial_update_width = math.ceil(transform.map(QLineF(0, 0, 1.5, 0)).length())

            inverted_event_rect = transform.inverted()[0].mapRect(QRectF(event.rect()))

            painter.save()
            painter.setTransform(transform)

            for c in range(len(self.plot.curves_x)):
                if not self.plot.curves_visible[c]:
                    continue

                curve_x = self.plot.curves_x[c]
                curve_y = self.plot.curves_y[c]
                path = QPainterPath()
                lineTo = path.lineTo
                start = max(min(bisect.bisect_left(curve_x, inverted_event_rect.left()), len(curve_x) - 1) - 1, 0)

                path.moveTo(curve_x[start], curve_y[start])

                for i in xrange(start + 1, len(curve_x)):
                    lineTo(curve_x[i], curve_y[i])

                painter.setPen(self.plot.configs[c][1])
                painter.drawPath(path)

            painter.restore()

class Plot(QWidget):
    def __init__(self, parent, y_scale_title_text, configs, scales_visible=True,
                 curve_outer_border_visible=True, curve_motion_granularity=10,
                 canvas_color=QColor(245, 245, 245)):
        QWidget.__init__(self, parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.configs = configs
        self.scales_visible = scales_visible
        self.history_length_x = 20 # seconds

        if curve_outer_border_visible:
            self.curve_outer_border = 5 # px, fixed
        else:
            self.curve_outer_border = 0 # px, fixed

        if sys.platform == 'darwin':
            # FIXME: there is a 1px vertical offset in the curve drawing on Mac OS X.
            #        it's not clear what the reason is, just workaround it for now
            self.curve_y_offset = 1
        else:
            self.curve_y_offset = 0

        self.curve_motion_granularity = curve_motion_granularity
        self.curve_to_scale = 8 # px, fixed
        self.cross_hair_visible = False
        self.canvas_color = canvas_color
        self.partial_update_width = 50 # px, initial value, calculated in update
        self.partial_update_enabled = False

        self.tick_text_font = self.font()

        self.title_text_font = self.font()
        self.title_text_font.setPointSize(round(self.title_text_font.pointSize() * 1.2))
        self.title_text_font.setBold(True)

        self.x_scale = XScale(self.tick_text_font, self.title_text_font, 'Time [s]')

        self.y_scale = YScale(self.tick_text_font, self.title_text_font, y_scale_title_text)
        self.y_scale_fixed = False
        self.y_scale_height_offset = max(self.curve_outer_border, self.y_scale.tick_text_height_half) # px, from top

        self.curve_area = CurveArea(self)
        self.y_scale.total_width_changed = self.resize_curve_area

        self.clear_graph()
        self.resize_curve_area()

    # override QWidget.sizeHint
    def sizeHint(self):
        return QSize(600, 300)

    # override QWidget.resizeEvent
    def resizeEvent(self, event):
        height = event.size().height()
        max_width = height - self.y_scale_height_offset - self.x_scale.total_height - self.curve_to_scale

        self.y_scale.update_title_text_height(max_width)

        QWidget.resizeEvent(self, event)

        self.resize_curve_area()

    # override QWidget.paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        if self.scales_visible:
            curve_width = width - self.y_scale.total_width - self.curve_to_scale - self.curve_outer_border
            curve_height = height - self.y_scale_height_offset - self.x_scale.total_height - self.curve_to_scale
        else:
            curve_width = width - self.curve_outer_border - self.curve_outer_border
            curve_height = height - self.curve_outer_border - self.curve_outer_border

        if DEBUG:
            painter.fillRect(0, 0, width, height, Qt.green)

        # fill canvas
        if self.scales_visible:
            canvas_x = self.y_scale.total_width + self.curve_to_scale - self.curve_outer_border
            canvas_y = self.y_scale_height_offset - self.curve_outer_border
        else:
            canvas_x = 0
            canvas_y = 0

        canvas_width = self.curve_outer_border + curve_width + self.curve_outer_border
        canvas_height = self.curve_outer_border + curve_height + self.curve_outer_border

        painter.fillRect(canvas_x, canvas_y, canvas_width, canvas_height, self.canvas_color)

        # draw cross hair at cursor position
        if self.cross_hair_visible:
            p = self.mapFromGlobal(QCursor.pos())
            p_x = p.x()
            p_y = p.y()

            if p_x >= canvas_x and p_x < canvas_x + canvas_width and \
               p_y >= canvas_y and p_y < canvas_y + canvas_height:
                painter.setPen(QPen(QColor(190, 190, 190), 1, Qt.DashLine))
                painter.drawLine(canvas_x, p_y, canvas_x + canvas_width - 1, p_y)
                painter.drawLine(p_x, canvas_y, p_x, canvas_y + canvas_height - 1)

        # draw canvas border
        if self.curve_outer_border > 0:
            painter.setPen(QColor(190, 190, 190))
            painter.drawRect(canvas_x, canvas_y, canvas_width - 1, canvas_height - 1) # -1 to accommodate the 1px width of the border
            painter.setPen(Qt.black)

        if DEBUG:
            painter.fillRect(canvas_x + self.curve_outer_border,
                             canvas_y + self.curve_outer_border,
                             curve_width,
                             curve_height,
                             Qt.cyan)

        # draw scales
        y_min_scale = self.y_scale.value_min
        y_max_scale = self.y_scale.value_max

        factor_x = float(curve_width) / self.history_length_x
        factor_y = float(curve_height - 1) / max(y_max_scale - y_min_scale, EPSILON) # -1 to accommodate the 1px width of the curve

        if self.scales_visible:
            self.draw_x_scale(painter, factor_x)
            self.draw_y_scale(painter, curve_height, factor_y)

    def resize_curve_area(self):
        if self.curve_area == None:
            return

        width = self.width()
        height = self.height()

        if self.scales_visible:
            curve_x = self.y_scale.total_width + self.curve_to_scale
            curve_y = self.y_scale_height_offset
            curve_width = width - self.y_scale.total_width - self.curve_to_scale - self.curve_outer_border
            curve_height = height - self.y_scale_height_offset - self.x_scale.total_height - self.curve_to_scale
        else:
            curve_x = self.curve_outer_border
            curve_y = self.curve_outer_border
            curve_width = width - self.curve_outer_border - self.curve_outer_border
            curve_height = height - self.curve_outer_border - self.curve_outer_border

        self.curve_area.setGeometry(curve_x, curve_y, curve_width, curve_height)

    def set_fixed_y_scale(self, value_min, value_max, step_size, step_division_count):
        self.y_scale_fixed = True
        self.y_scale.update_tick_config(value_min, value_max, step_size, step_division_count)

    def get_legend_offset_y(self): # px, from top
        return max(self.y_scale.tick_text_height_half - self.curve_outer_border, 0)

    def draw_x_scale(self, painter, factor):
        offset_x = self.y_scale.total_width + self.curve_to_scale
        offset_y = self.height() - self.x_scale.total_height

        if self.x_min != None:
            x_min = self.x_min
        else:
            x_min = 0

        painter.save()
        painter.translate(offset_x, offset_y)

        self.x_scale.draw(painter, factor, x_min, self.history_length_x)

        painter.restore()

    def draw_y_scale(self, painter, height, factor):
        offset_x = self.y_scale.total_width
        offset_y = self.height() - self.x_scale.total_height - self.curve_to_scale - 1

        painter.save()
        painter.translate(offset_x, offset_y)

        self.y_scale.draw(painter, height, factor)

        painter.restore()

    # NOTE: assumes that x is a timestamp in seconds that constantly grows
    def add_data(self, c, x, y):
        if self.y_type == None:
            self.y_type = type(y)

        x = float(x)
        y = float(y)

        last_y_min = self.y_min
        last_y_max = self.y_max

        if self.x_min == None:
            self.x_min = x

        if self.x_max == None:
            self.x_max = x

        if self.curves_visible[c]:
            if self.y_min == None:
                self.y_min = y
            else:
                self.y_min = min(self.y_min, y)

            if self.y_max == None:
                self.y_max = y
            else:
                self.y_max = max(self.y_max, y)

        self.curves_x[c].append(x)
        self.curves_y[c].append(y)

        if self.curves_x_min[c] == None:
            self.curves_x_min[c] = x

        if self.curves_x_max[c] == None:
            self.curves_x_max[c] = x

        if self.curves_y_min[c] == None:
            self.curves_y_min[c] = y
        else:
            self.curves_y_min[c] = min(self.curves_y_min[c], y)

        if self.curves_y_max[c] == None:
            self.curves_y_max[c] = y
        else:
            self.curves_y_max[c] = max(self.curves_y_max[c], y)

        if len(self.curves_x[c]) > 0:
            if (self.curves_x[c][-1] - self.curves_x[c][0]) >= self.history_length_x:
                self.curves_x[c] = self.curves_x[c][self.curve_motion_granularity:]
                self.curves_y[c] = self.curves_y[c][self.curve_motion_granularity:]

                if len(self.curves_x[c]) > 0:
                    self.curves_x_min[c] = self.curves_x[c][0]
                else:
                    self.curves_x_min[c] = None

                if len(self.curves_x[c]) > 0:
                    self.curves_x_max[c] = self.curves_x[c][-1]
                else:
                    self.curves_x_max[c] = None

                self.curves_y_min[c] = min(self.curves_y[c])
                self.curves_y_max[c] = max(self.curves_y[c])

                self.update_x_min_max_y_min_max()

                self.partial_update_enabled = True
            else:
                self.curves_x_max[c] = self.curves_x[c][-1]
                self.x_max = min(self.curves_x_max)

        if self.curves_visible[c] and (last_y_min != self.y_min or last_y_max != self.y_max):
            self.update_y_min_max_scale()

        if self.partial_update_enabled:
            self.curve_area.update(self.curve_area.width() - self.partial_update_width, 0, self.partial_update_width, self.curve_area.height())
        else:
            self.curve_area.update()

    def update_x_min_max_y_min_max(self):
        last_x_min, last_x_max, last_y_min, last_y_max = self.x_min, self.x_max, self.y_min, self.y_max

        self.x_min = min(self.curves_x_min)
        self.x_max = min(self.curves_x_max)

        if sum(map(int, self.curves_visible)) > 0:
            self.y_min = min([curve_y_min for k, curve_y_min in enumerate(self.curves_y_min) if self.curves_visible[k]])
            self.y_max = max([curve_y_max for k, curve_y_max in enumerate(self.curves_y_max) if self.curves_visible[k]])
        else:
            self.y_min = None
            self.y_max = None

        if (last_x_min, last_x_max, last_y_min, last_y_max) != (self.x_min, self.x_max, self.y_min, self.y_max):
            self.update()
            self.curve_area.update()

    def update_y_min_max_scale(self):
        if self.y_scale_fixed:
            return

        if self.y_min == None or self.y_max == None:
            y_min = -1.0
            y_max = 1.0
        else:
            y_min = self.y_min
            y_max = self.y_max

        delta_y = abs(y_max - y_min)

        # if there is no delta then force some to get a y-axis with some ticks
        if delta_y < EPSILON:
            delta_y = 2.0
            y_min -= 1.0
            y_max += 1.0

        # start with the biggest power of 10 that is smaller than delta-y
        step_size = 10.0 ** math.floor(math.log(delta_y, 10.0))
        step_subdivision_count = 5

        # the divisors are chosen in way to produce the sequence
        # 100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05 etc
        divisors = [2.0, 2.5, 2.0]
        subdivisions = [5, 4, 5]
        d = 0

        if self.y_type == int:
            step_size_min = 1.0
        else:
            step_size_min = EPSILON

        # decrease y-axis step-size until it divides delta-y in 4 or more parts
        while fuzzy_geq(step_size / divisors[d % len(divisors)], step_size_min) \
              and delta_y / step_size < 4.0:
            step_size /= divisors[d % len(divisors)]
            step_subdivision_count = subdivisions[d % len(subdivisions)]
            d += 1

        if d == 0:
            # if no division occurred in the first while loop then add 1
            # to d to counter the d -= 1 in the next while loop
            d += 1

        # increase y-axis step-size until it divides delta-y in 8 or less parts
        while delta_y / step_size > 8.0:
            step_subdivision_count = subdivisions[d % len(subdivisions)]
            d -= 1
            step_size *= divisors[d % len(divisors)]

        # ensure that the y-axis endpoints are multiple of the step-size
        y_min_scale = math.floor(y_min / step_size) * step_size
        y_max_scale = math.ceil(y_max / step_size) * step_size

        # fix rounding (?) errors from floor/ceil scaling
        while fuzzy_leq(y_min_scale + step_size, y_min):
            y_min_scale += step_size

        while fuzzy_geq(y_max_scale - step_size, y_max):
            y_max_scale -= step_size

        # if the y-axis endpoints are identical then force them 4 steps apart
        if fuzzy_eq(y_min_scale, y_max_scale):
            y_min_scale -= 2.0 * step_size
            y_max_scale += 2.0 * step_size

        self.y_scale.update_tick_config(y_min_scale, y_max_scale,
                                        step_size, step_subdivision_count)

        self.update()
        self.curve_area.update()

    def show_curve(self, c, show):
        if self.curves_visible[c] == show:
            return

        last_y_min = self.y_min
        last_y_max = self.y_max

        self.curves_visible[c] = show

        self.update_x_min_max_y_min_max()

        if last_y_min != self.y_min or last_y_max != self.y_max:
            self.update_y_min_max_scale()

        self.update()
        self.curve_area.update()

    def clear_graph(self):
        count = len(self.configs)

        if not hasattr(self, 'curves_visible'):
            self.curves_visible = [True]*count # per curve visibility

        def new_list():
            return []

        self.curves_x = [new_list() for i in range(count)] # per curve x values
        self.curves_y = [new_list() for i in range(count)] # per curve y values
        self.curves_x_min = [None]*count # per curve minimum x value
        self.curves_x_max = [None]*count # per curve maximum x value
        self.curves_y_min = [None]*count # per curve minimum y value
        self.curves_y_max = [None]*count # per curve maximum y value
        self.x_min = None # minimum x value over all curves
        self.x_max = None # maximum x value over all curves
        self.y_min = None # minimum y value over all curves
        self.y_max = None # maximum y value over all curves
        self.y_type = None
        self.partial_update_enabled = False

        self.update()
        self.curve_area.update()

class FixedSizeToolButton(QToolButton):
    maximum_size_hint = None

    def sizeHint(self):
        hint = QToolButton.sizeHint(self)

        if self.maximum_size_hint != None:
            hint = QSize(max(hint.width(), self.maximum_size_hint.width()),
                         max(hint.height(), self.maximum_size_hint.height()))

        self.maximum_size_hint = hint

        return hint

class FixedSizeLabel(QLabel):
    maximum_size_hint = None

    def sizeHint(self):
        hint = QLabel.sizeHint(self)

        if self.maximum_size_hint != None:
            hint = QSize(max(hint.width(), self.maximum_size_hint.width()),
                         max(hint.height(), self.maximum_size_hint.height()))

        self.maximum_size_hint = hint

        return hint

class PlotWidget(QWidget):
    def __init__(self, y_scale_title_text, configs, clear_button=None, parent=None,
                 scales_visible=True, curve_outer_border_visible=True,
                 curve_motion_granularity=10, canvas_color=QColor(245, 245, 245),
                 external_timer=None, key='top-value', extra_key_widgets=None,
                 update_interval=0.1):
        QWidget.__init__(self, parent)

        self.setMinimumSize(300, 250)

        self.stop = True
        self.plot = Plot(self, y_scale_title_text, configs, scales_visible,
                         curve_outer_border_visible, curve_motion_granularity,
                         canvas_color)
        self.set_fixed_y_scale = self.plot.set_fixed_y_scale
        self.key = key
        self.key_items = []
        self.key_has_values = key.endswith('-value') if key != None else False
        self.first_show = True
        self.timestamp = 0 # seconds
        self.update_interval = update_interval # seconds
        self.configs = configs

        h1layout = QHBoxLayout()
        h1layout.setContentsMargins(0, 0, 0, 0)

        if clear_button == None:
            self.clear_button = QToolButton()
            self.clear_button.setText('Clear Graph')
            h1layout.addWidget(self.clear_button)
        else:
            self.clear_button = clear_button

        self.clear_button.clicked.connect(self.clear_clicked)

        h1layout.addStretch(1)

        v1layout = None

        if self.key != None:
            if len(self.configs) == 1:
                label = FixedSizeLabel(self)
                label.setText(self.configs[0][0])

                self.key_items.append(label)
            else:
                for i, config in enumerate(self.configs):
                    pixmap = QPixmap(10, 1)
                    QPainter(pixmap).fillRect(0, 0, 10, 1, config[1])

                    button = FixedSizeToolButton(self)
                    button.setText(config[0])
                    button.setIcon(QIcon(pixmap))
                    button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                    button.setCheckable(True)
                    button.setChecked(True)
                    button.toggled.connect(functools.partial(self.plot.show_curve, i))

                    self.key_items.append(button)

            if self.key.startswith('top'):
                for key_item in self.key_items:
                    h1layout.addWidget(key_item)
            elif self.key.startswith('right'):
                v1layout = QVBoxLayout()
                v1layout.setContentsMargins(0, 0, 0, 0)
                v1layout.addSpacing(self.plot.get_legend_offset_y())

                for key_item in self.key_items:
                    v1layout.addWidget(key_item)

                v1layout.addStretch(1)

        h1layout.addStretch(1)

        if extra_key_widgets != None:
            if self.key.startswith('top'):
                for widget in extra_key_widgets:
                    h1layout.addWidget(widget)
            elif self.key.startswith('right'):
                if v1layout == None:
                    v1layout = QVBoxLayout()
                    v1layout.setContentsMargins(0, 0, 0, 0)
                    v1layout.addSpacing(self.plot.get_legend_offset_y())

                if self.key.startswith('top'):
                    for widget in extra_key_widgets:
                        v1layout.addWidget(widget)

        v2layout = QVBoxLayout(self)
        v2layout.setContentsMargins(0, 0, 0, 0)

        if h1layout.count() > 2:
            v2layout.addLayout(h1layout)

        if v1layout != None:
            h2layout = QHBoxLayout()
            h2layout.setContentsMargins(0, 0, 0, 0)

            h2layout.addWidget(self.plot)
            h2layout.addLayout(v1layout)

            v2layout.addLayout(h2layout)
        else:
            v2layout.addWidget(self.plot)

        if external_timer == None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.add_new_data)
            self.timer.start(self.update_interval * 1000)
        else:
            # assuming that the external timer runs with the configured interval
            external_timer.timeout.connect(self.add_new_data)

    # overrides QWidget.showEvent
    def showEvent(self, event):
        QWidget.showEvent(self, event)

        if self.first_show:
            self.first_show = False

            if len(self.key_items) > 1 and self.key.startswith('right'):
                widths = []

                for key_item in self.key_items:
                    widths.append(key_item.width())

                width = max(widths)

                for key_item in self.key_items:
                    size = key_item.minimumSize()

                    size.setWidth(width)

                    key_item.setMinimumSize(size)

    def get_key_item(self, i):
        return self.key_items[i]

    # internal
    def add_new_data(self):
        if self.stop:
            return

        for i, config in enumerate(self.configs):
            value = config[2]()

            if value != None:
                if len(self.key_items) > 0 and self.key_has_values:
                    self.key_items[i].setText(config[0] + ': ' + config[3](value))

                self.plot.add_data(i, self.timestamp, value)
            elif len(self.key_items) > 0 and self.key_has_values:
                self.key_items[i].setText(config[0])

        self.timestamp += self.update_interval

    # internal
    def clear_clicked(self):
        self.plot.clear_graph()
        self.counter = 0
