# -*- coding: utf-8 -*-
"""
Industrial Digital Out 4 Plugin
Copyright (C) 2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

industrial_digital_out_4.py: Industrial Digital Out 4 Plugin Implementation

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

import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QComboBox

from brickv.plugin_system.plugin_base import PluginBase
from brickv.plugin_system.plugins.industrial_digital_out_4.ui_industrial_digital_out_4 import Ui_IndustrialDigitalOut4
from brickv.bindings.bricklet_industrial_digital_out_4 import BrickletIndustrialDigitalOut4
from brickv.async_call import async_call
from brickv.load_pixmap import load_masked_pixmap
from brickv.monoflop import Monoflop

class IndustrialDigitalOut4(PluginBase, Ui_IndustrialDigitalOut4):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickletIndustrialDigitalOut4, *args)

        self.setupUi(self)

        self.ido4 = self.device

        self.gnd_pixmap = load_masked_pixmap('plugin_system/plugins/industrial_digital_out_4/dio_gnd.bmp')
        self.vcc_pixmap = load_masked_pixmap('plugin_system/plugins/industrial_digital_out_4/dio_vcc.bmp')

        self.pin_buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9, self.b10, self.b11, self.b12, self.b13, self.b14, self.b15]
        self.pin_button_icons = [self.b0_icon, self.b1_icon, self.b2_icon, self.b3_icon, self.b4_icon, self.b5_icon, self.b6_icon, self.b7_icon, self.b8_icon, self.b9_icon, self.b10_icon, self.b11_icon, self.b12_icon, self.b13_icon, self.b14_icon, self.b15_icon]
        self.pin_button_labels = [self.b0_label, self.b1_label, self.b2_label, self.b3_label, self.b4_label, self.b5_label, self.b6_label, self.b7_label, self.b8_label, self.b9_label, self.b10_label, self.b11_label, self.b12_label, self.b13_label, self.b14_label, self.b15_label]
        self.groups = [self.group0, self.group1, self.group2, self.group3]

        for icon in self.pin_button_icons:
            icon.setPixmap(self.gnd_pixmap)
            icon.show()

        self.lines = [[self.line0, self.line0a, self.line0b, self.line0c],
                      [self.line1, self.line1a, self.line1b, self.line1c],
                      [self.line2, self.line2a, self.line2b, self.line2c],
                      [self.line3, self.line3a, self.line3b, self.line3c]]

        for lines in self.lines:
            for line in lines:
                line.setVisible(False)

        self.available_ports = 0

        for i in range(len(self.pin_buttons)):
            self.pin_buttons[i].clicked.connect(functools.partial(self.pin_button_clicked, i))

        self.monoflop_states = []
        self.monoflop_times = []

        for i in range(16):
            monoflop_state = QComboBox()
            monoflop_state.addItem('High', 1)
            monoflop_state.addItem('Low', 0)

            self.monoflop_states.append(monoflop_state)
            self.monoflop_state_stack.addWidget(monoflop_state)

            monoflop_time = QSpinBox()
            monoflop_time.setRange(1, (1 << 31) - 1)
            monoflop_time.setValue(1000)

            self.monoflop_times.append(monoflop_time)
            self.monoflop_time_stack.addWidget(monoflop_time)

        self.monoflop = Monoflop(self.ido4,
                                 list(range(16)),
                                 self.monoflop_states,
                                 self.cb_state_change_by_monoflop,
                                 self.monoflop_times,
                                 None,
                                 self,
                                 setter_uses_bitmasks=True,
                                 callback_uses_bitmasks=True,
                                 handle_get_monoflop_invalid_parameter_as_abort=True)

        self.set_group.clicked.connect(self.set_group_clicked)

        self.monoflop_pin.currentIndexChanged.connect(self.monoflop_pin_changed)
        self.monoflop_go.clicked.connect(self.monoflop_go_clicked)

    def start(self):
        self.reconfigure_everything()

    def stop(self):
        self.monoflop.stop()

    def destroy(self):
        pass

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletIndustrialDigitalOut4.DEVICE_IDENTIFIER

    def get_value_async(self, value_mask):
        for pin in range(16):
            if value_mask & (1 << pin):
                self.pin_buttons[pin].setText('Switch Low')
                self.pin_button_icons[pin].setPixmap(self.vcc_pixmap)
            else:
                self.pin_buttons[pin].setText('Switch High')
                self.pin_button_icons[pin].setPixmap(self.gnd_pixmap)

    def get_group_async(self, group):
        for i in range(4):
            if group[i] == 'n':
                self.groups[i].setCurrentIndex(0)
            else:
                item = 'Port ' + group[i].upper()
                index = self.groups[i].findText(item, Qt.MatchStartsWith)

                if index == -1:
                    self.groups[i].setCurrentIndex(0)
                else:
                    self.groups[i].setCurrentIndex(index)

        self.monoflop_pin.clear()

        if group[0] == 'n' and group[1] == 'n' and group[2] == 'n' and group[3] == 'n':
            self.show_buttons(0)
            self.hide_buttons(1)
            self.hide_buttons(2)
            self.hide_buttons(3)

            for pin in range(4):
                self.monoflop_pin.addItem('Pin {0}'.format(pin), pin)
        else:
            for i in range(4):
                if group[i] == 'n':
                    self.hide_buttons(i)
                else:
                    for j in range(4):
                        pin = i * 4 + j

                        self.monoflop_pin.addItem('Pin {0}'.format(pin), pin)

                    self.show_buttons(i)

        self.monoflop_pin.setCurrentIndex(0)

        async_call(self.ido4.get_value, None, self.get_value_async, self.increase_error_count)

        self.monoflop.start()

    def get_available_for_group_aysnc(self, available_ports):
        self.available_ports = available_ports

        for i in range(4):
            self.groups[i].clear()
            self.groups[i].addItem('Off')

            for j in range(4):
                if self.available_ports & (1 << j):
                    item = 'Port ' + chr(ord('A') + j)
                    self.groups[i].addItem(item)

        async_call(self.ido4.get_group, None, self.get_group_async, self.increase_error_count)

    def reconfigure_everything(self):
        async_call(self.ido4.get_available_for_group, None, self.get_available_for_group_aysnc, self.increase_error_count)

    def show_buttons(self, num):
        for i in range(num * 4, (num + 1) * 4):
            self.pin_buttons[i].setVisible(True)
            self.pin_button_icons[i].setVisible(True)
            self.pin_button_labels[i].setVisible(True)

        for line in self.lines[num]:
            line.setVisible(True)

    def hide_buttons(self, num):
        for i in range(num * 4, (num + 1) * 4):
            self.pin_buttons[i].setVisible(False)
            self.pin_button_icons[i].setVisible(False)
            self.pin_button_labels[i].setVisible(False)

        for line in self.lines[num]:
            line.setVisible(False)

    def set_group_clicked(self):
        group = ['n', 'n', 'n', 'n']

        for i in range(len(self.groups)):
            text = self.groups[i].currentText()
            if 'Port A' in text:
                group[i] = 'a'
            elif 'Port B' in text:
                group[i] = 'b'
            elif 'Port C' in text:
                group[i] = 'c'
            elif 'Port D' in text:
                group[i] = 'd'

        if group != ['n', 'n', 'n', 'n']:
            abort_group = group
        else:
            abort_group = ['x', 'n', 'n', 'n']

        for i, g in enumerate(abort_group):
            if g == 'n':
                for j in range(4):
                    pin = i * 4 + j

                    # changing grouping doesn't abort active monoflops. manually
                    # abort tracking for monoflops that are out of scope now
                    self.monoflop.abort_tracking(pin)

        self.ido4.set_group(group)
        self.reconfigure_everything()

    def pin_button_clicked(self, button):
        selection = 1 << button
        value = 0

        if 'High' in self.pin_buttons[button].text().replace('&', ''):
            value |= 1 << button
            self.pin_buttons[button].setText('Switch Low')
            self.pin_button_icons[button].setPixmap(self.vcc_pixmap)
        else:
            self.pin_buttons[button].setText('Switch High')
            self.pin_button_icons[button].setPixmap(self.gnd_pixmap)

        async_call(self.ido4.set_selected_values, (selection, value), None, self.increase_error_count)

    def cb_state_change_by_monoflop(self, pin, state):
        if state:
            self.pin_buttons[pin].setText('Switch Low')
            self.pin_button_icons[pin].setPixmap(self.vcc_pixmap)
        else:
            self.pin_buttons[pin].setText('Switch High')
            self.pin_button_icons[pin].setPixmap(self.gnd_pixmap)

    def monoflop_pin_changed(self):
        pin = self.monoflop_pin.currentData()

        if pin == None:
            return

        self.monoflop_time_stack.setCurrentIndex(pin)
        self.monoflop_state_stack.setCurrentIndex(pin)

    def monoflop_go_clicked(self):
        pin = self.monoflop_pin.currentData()

        if pin == None:
            return

        self.monoflop.trigger(pin)
