#!/usr/bin/env python3
# coding=utf-8

from PyCRC.CRC16 import CRC16
import smbus
import time
import copy

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTimer
from hmi import Ui_MainWindow

import func.function as calculate 

class exampleapp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(exampleapp, self).__init__(parent)
        self.setupUi(self)
        self.i2c_to = smbus.SMBus(1)
        self.pi2c = i2c_process()
        self.addr_rx = 0x08
        self.addr_tx = 0x08

        self.cnt = 0

    #def slot1(self):
    #   self.setWindowTitle('heelloo')

    def tick(self):
        self.cnt += 1
        string = 'heelloo' + str(self.cnt)
        self.setWindowTitle(string)
        self.update_data()

        # rx
        self.lineEdit_data_Vrect.setText(str(round(self.pi2c.rx_ds.result['Vrect'], 3))) 
        self.lineEdit_data_Vcha.setText(str(round(self.pi2c.rx_ds.result['Vcha'], 3))) 
        self.lineEdit_data_Fsk_dem.setText(str(round(self.pi2c.rx_ds.result['FSK'], 3))) 
        self.lineEdit_data_Irect.setText(str(round(self.pi2c.rx_ds.result['Irect'], 3))) 
        self.lineEdit_data_Icha.setText(str(round(self.pi2c.rx_ds.result['Icha'], 3))) 
        self.lineEdit_data_Treboard.setText(str(round(self.pi2c.rx_ds.result['Trxboard'], 3))) 

        if self.pi2c.rx_ds.over['Vsens'] == 1:
            self.checkBox_state_overVsens.setChecked(True)
        else:
            self.checkBox_state_overVsens.setChecked(False)

        if self.pi2c.rx_ds.over['VsensCHA'] == 1:
            self.checkBox_state_overVsensCHA.setChecked(True)
        else:
            self.checkBox_state_overVsensCHA.setChecked(False)

        if self.pi2c.rx_ds.over['FSKdem'] == 1:
            self.checkBox_state_overFsk_dem.setChecked(True)
        else:
            self.checkBox_state_overFsk_dem.setChecked(False)
            
        if self.pi2c.rx_ds.under['Vsens'] == 1:
            self.checkBox_state_underVsens.setChecked(True)
        else:
            self.checkBox_state_underVsens.setChecked(False)  

        if self.pi2c.rx_ds.under['VsensCHA'] == 1:
            self.checkBox_state_underVsensCHA.setChecked(True)
        else:
            self.checkBox_state_underVsensCHA.setChecked(False)
            
        if self.pi2c.rx_ds.under['FSKdem'] == 1:
            self.checkBox_state_underFsk_dem.setChecked(True)
        else:
            self.checkBox_state_underFsk_dem.setChecked(False)  
            
        if self.pi2c.rx_ds.low['Isens'] == 1:
            self.checkBox_state_lowIsens.setChecked(True)
        else:
            self.checkBox_state_lowIsens.setChecked(False)
            
        if self.pi2c.rx_ds.low['IsensCHA'] == 1:
            self.checkBox_state_lowIsensCHA.setChecked(True)
        else:
            self.checkBox_state_lowIsensCHA.setChecked(False)  
            
        if self.pi2c.rx_ds.over['Tsens'] == 1:
            self.checkBox_state_overTsens.setChecked(True)
        else:
            self.checkBox_state_overTsens.setChecked(False)  
            
        if self.pi2c.rx_ds.under['Tsens'] == 1:
            self.checkBox_state_underTsens.setChecked(True)
        else:
            self.checkBox_state_underTsens.setChecked(False)

        self.lineEdit_thd_overVsens.setText(str(round(self.pi2c.rx_ds.thd_over['Vsens'], 3))) 
        self.lineEdit_thd_overVsensCHA.setText(str(round(self.pi2c.rx_ds.thd_over['VsensCHA'], 3)))     
        self.lineEdit_thd_overFsk_dem.setText(str(round(self.pi2c.rx_ds.thd_over['FSKdem'], 3)))
        self.lineEdit_thd_underVsens.setText(str(round(self.pi2c.rx_ds.thd_under['Vsens'], 3)))
        self.lineEdit_thd_underVsensCHA.setText(str(round(self.pi2c.rx_ds.thd_under['VsensCHA'], 3)))     
        self.lineEdit_thd_underFsk_dem.setText(str(round(self.pi2c.rx_ds.thd_under['FSKdem'], 3)))
        self.lineEdit_thd_lowIsens.setText(str(round(self.pi2c.rx_ds.thd_low['Isens'], 3)))
        self.lineEdit_thd_lowIsensCHA.setText(str(round(self.pi2c.rx_ds.thd_low['IsensCHA'], 3)))     
        self.lineEdit_thd_overTsens.setText(str(round(self.pi2c.rx_ds.thd_over['Tsens'], 3)))
        self.lineEdit_thd_underTsens.setText(str(round(self.pi2c.rx_ds.thd_under['Tsens'], 3)))

        # tx
        self.lineEdit_tx_data_DCin.setText(str(round(self.pi2c.tx_ds.result['DCin'], 3))) 
        self.lineEdit_tx_data_AC_dem.setText(str(round(self.pi2c.tx_ds.result['Vcoil'], 3))) 
        self.lineEdit_tx_data_Lin.setText(str(round(self.pi2c.tx_ds.result['Iin'], 3))) 
        self.lineEdit_tx_data_Ttxboard.setText(str(round(self.pi2c.tx_ds.result['Ttxboard'], 3)))

        if self.pi2c.tx_ds.over['Vsens'] == 1:
            self.checkBox_tx_state_overVsens.setChecked(True)
        else:
            self.checkBox_tx_state_overVsens.setChecked(False)
        if self.pi2c.tx_ds.over['ACdem'] == 1:
            self.checkBox_tx_state_overACdem.setChecked(True)
        else:
            self.checkBox_tx_state_overACdem.setChecked(False)
        if self.pi2c.tx_ds.under['Vsens'] == 1:
            self.checkBox_tx_state_underVsens.setChecked(True)
        else:
            self.checkBox_tx_state_underVsens.setChecked(False)
        if self.pi2c.tx_ds.under['ACdem'] == 1:
            self.checkBox_tx_state_underACdem.setChecked(True)
        else:
            self.checkBox_tx_state_underACdem.setChecked(False)
        if self.pi2c.tx_ds.low['Isens'] == 1:
            self.checkBox_tx_state_lowIsens.setChecked(True)
        else:
            self.checkBox_tx_state_lowIsens.setChecked(False)
        if self.pi2c.tx_ds.over['Tsens'] == 1:
            self.checkBox_tx_state_overTsens.setChecked(True)
        else:
            self.checkBox_tx_state_overTsens.setChecked(False)
        if self.pi2c.tx_ds.under['Tsens'] == 1:
            self.checkBox_tx_state_underTsens.setChecked(True)
        else:
            self.checkBox_tx_state_underTsens.setChecked(False)

        self.lineEdit_tx_thd_overVsens.setText(str(round(self.pi2c.tx_ds.thd_over['Vsens'], 3))) 
        self.lineEdit_tx_thd_overAC_dem.setText(str(round(self.pi2c.tx_ds.thd_over['ACdem'], 3)))
        self.lineEdit_tx_thd_underVsens.setText(str(round(self.pi2c.tx_ds.thd_under['Vsens'], 3)))
        self.lineEdit_tx_thd_underAC_dem.setText(str(round(self.pi2c.tx_ds.thd_under['ACdem'], 3)))
        self.lineEdit_tx_thd_lowIsens.setText(str(round(self.pi2c.tx_ds.thd_low['Isens'], 3)))
        self.lineEdit_tx_thd_overTsens.setText(str(round(self.pi2c.tx_ds.thd_over['Tsens'], 3)))
        self.lineEdit_tx_thd_underTsens.setText(str(round(self.pi2c.tx_ds.thd_under['Tsens'], 3)))
            
    
    def update_data(self):
        # rx: GetData
        cmd = 'GetData'
        send_values = self.pi2c.encode('rx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_rx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_rx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('rx', cmd, recv_value)

        # rx: GetStat
        cmd = 'GetStat'
        send_values = self.pi2c.encode('rx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_rx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_rx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('rx', cmd, recv_value)

        # rx: GetThd
        cmd = 'GetThd'
        send_values = self.pi2c.encode('rx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_rx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_rx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('rx', cmd, recv_value)

        # tx: GetData
        cmd = 'GetData'
        send_values = self.pi2c.encode('tx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_tx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_tx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('tx', cmd, recv_value)

        # tx: GetStat
        cmd = 'GetStat'
        send_values = self.pi2c.encode('tx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_tx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_tx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('tx', cmd, recv_value)
        
        # tx: GetThd
        cmd = 'GetThd'
        send_values = self.pi2c.encode('tx', cmd)
        reg = send_values[0]

        self.i2c_to.write_i2c_block_data(self.addr_tx, reg, send_values[1:])

        time.sleep(0.3)

        recv_value = self.i2c_to.read_i2c_block_data(self.addr_tx, reg)
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        recv_value = recv_value[0: recv_value[1]]
        print('recv_value = [{}]'.format(', '.join(hex(x) for x in recv_value)))

        self.pi2c.decode('tx', cmd, recv_value)

class data_structure():
    def __str__(self):
        return "Data structure."

    def __init__(self, type):
        keys = ['Vsens', 'Isens', 'Tsens']
        self.normal = dict().fromkeys(keys)
        self.over = dict().fromkeys(keys)
        self.under = dict().fromkeys(keys)
        self.low = dict().fromkeys(['Isens'])
        self.control = dict()
        self.result = dict()
        
        self.thd_over = dict().fromkeys(keys)
        self.thd_under = dict().fromkeys(keys)
        self.thd_low = dict().fromkeys(['Isens'])

        if type is 'tx':
            self.normal.setdefault('ACdem')
            self.over.setdefault('ACdem')
            del self.over['Isens']
            self.under.setdefault('ACdem')
            del self.under['Isens']
            self.control = dict().fromkeys(['STpwm'])
            self.result = dict().fromkeys(['DCin', 'Vcoil', 'Iin', 'Ttxboard'])

            self.thd_over.setdefault('ACdem')
            del self.thd_over['Isens']
            self.thd_under.setdefault('ACdem')
            del self.thd_under['Isens']
            
        elif type is 'rx':
            self.normal.setdefault('VsensCHA')
            self.normal.setdefault('IsensCHA')
            self.normal.setdefault('FSKdem')
            self.over.setdefault('VsensCHA')
            self.over.setdefault('FSKdem')
            del self.over['Isens']
            self.under.setdefault('VsensCHA')
            self.under.setdefault('FSKdem')
            del self.under['Isens']
            self.low.setdefault('IsensCHA')
            self.control = dict().fromkeys(['Clam', 'ACcomm', 'OUTen'])
            self.result = dict().fromkeys(['Vrect', 'Vcha', 'FSK', 'Irect', 'Icha', 'Trxboard'])

            self.thd_over.setdefault('VsensCHA')
            self.thd_over.setdefault('FSKdem')
            del self.thd_over['Isens']
            self.thd_under.setdefault('VsensCHA')
            self.thd_under.setdefault('FSKdem')
            del self.thd_under['Isens']
            self.thd_low.setdefault('IsensCHA')

        # print('{}: normal: {}'.format(type, self.normal))
        # print('{}: over: {}'.format(type, self.over))
        # print('{}: under: {}'.format(type, self.under))
        # print('{}: low: {}'.format(type, self.low))
        # print('{}: control: {}'.format(type, self.low))


class i2c_process:
    def __str__(self):
        return "Process and store data."

    def __init__(self):
        self.tx_ds = data_structure('tx')
        self.rx_ds = data_structure('rx')

    def encode(self, slave_type, cmd):
        data = list()

        if slave_type == 'rx':
            if cmd is 'GetData':
                para = [0x40, 0x04]
                data.extend(para)
            elif cmd is 'GetStat':
                para = [0x41, 0x04]
                data.extend(para)
            elif cmd is 'GetThd':
                para = [0x42, 0x04]
                data.extend(para)
        else:
            if cmd is 'GetData':
                para = [0x50, 0x04]
                data.extend(para)
            elif cmd is 'GetStat':
                para = [0x51, 0x04]
                data.extend(para)
            elif cmd is 'GetThd':
                para = [0x52, 0x04]
                data.extend(para)

        high, low = divmod(int(hex(CRC16(modbus_flag=True).calculate(bytes(data))), 0), 0x100)
        data.extend([high, low])

        print('\nCMD = [{}], high, low = {}, {}'.format(', '.join(hex(x) for x in data), high, low))
        return data

    def decode(self, slave_type, cmd, data):
        local_data = copy.deepcopy(data)
        print('local_data = [{}]'.format(', '.join(hex(x) for x in local_data)))

        crc = hex(CRC16(modbus_flag=True).calculate(bytes(local_data[0:-2])))
        high, low = divmod(int(crc, 0), 0x100)
        print(hex(high), hex(low))

        ret = False
        if (local_data[-2] is high) and (local_data[-1] is low):
            print('CRC correct!')
            # rx
            if local_data[0] == 0x4A:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))

                self.rx_ds.normal['Vsens'] = ((value[0]<<8)|value[1])/100
                self.rx_ds.normal['Isens'] = ((value[2]<<8)|value[3])/100
                self.rx_ds.normal['Tsens'] = ((value[4]<<8)|value[5])/100
                self.rx_ds.normal['VsensCHA'] = ((value[6]<<8)|value[7])/100
                self.rx_ds.normal['IsensCHA'] = ((value[8]<<8)|value[9])/100
                self.rx_ds.normal['FSKdem'] = ((value[8]<<8)|value[9])/100
                print('rx normal = {}'.format(self.rx_ds.normal))

                self.rx_ds.result['Vrect'] = 31 * self.rx_ds.normal['Vsens']
                self.rx_ds.result['Vcha'] = 31 * self.rx_ds.normal['VsensCHA']
                self.rx_ds.result['FSK'] = 1 * self.rx_ds.normal['FSKdem']
                self.rx_ds.result['Irect'] = 1 * self.rx_ds.normal['Isens']
                self.rx_ds.result['Icha'] = 1 * self.rx_ds.normal['IsensCHA']
                self.rx_ds.result['Trxboard'] = 1 * self.rx_ds.normal['Tsens']
                print('rx result = {}'.format(self.rx_ds.result))

            elif local_data[0] == 0x4B:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))
                stat = '{:b}'.format(value[0]).zfill(8) + '{:b}'.format(value[1]).zfill(8)
                stat = stat[:-6]
                print('stat = [{}]'.format(stat))

                self.rx_ds.over['Vsens'] = int(stat[0])
                self.rx_ds.over['VsensCHA'] = int(stat[1])
                self.rx_ds.over['FSKdem'] = int(stat[2])
                self.rx_ds.under['Vsens'] = int(stat[3])
                self.rx_ds.under['VsensCHA'] = int(stat[4])
                self.rx_ds.under['FSKdem'] = int(stat[5])
                self.rx_ds.low['Isens'] = int(stat[6])
                self.rx_ds.low['IsensCHA'] = int(stat[7])
                self.rx_ds.over['Tsens'] = int(stat[8])
                self.rx_ds.under['Tsens'] = int(stat[9])

                print('rx over = {}'.format(self.rx_ds.over))
                print('rx under = {}'.format(self.rx_ds.under))
                print('rx low = {}'.format(self.rx_ds.low))

            elif local_data[0] == 0x4C:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))
                
                self.rx_ds.thd_over['Vsens'] = ((value[0]<<8)|value[1])/100
                self.rx_ds.thd_over['VsensCHA'] = ((value[2]<<8)|value[3])/100
                self.rx_ds.thd_over['FSKdem'] = ((value[4]<<8)|value[5])/100
                self.rx_ds.thd_under['Vsens'] = ((value[6]<<8)|value[7])/100
                self.rx_ds.thd_under['VsensCHA'] = ((value[8]<<8)|value[9])/100
                self.rx_ds.thd_under['FSKdem'] = ((value[10]<<8)|value[11])/100
                self.rx_ds.thd_low['Isens'] = ((value[12]<<8)|value[13])/100
                self.rx_ds.thd_low['IsensCHA'] = ((value[14]<<8)|value[15])/100
                self.rx_ds.thd_over['Tsens'] = ((value[16]<<8)|value[17])/100
                self.rx_ds.thd_under['Tsens'] = ((value[18]<<8)|value[19])/100

            # tx
            elif local_data[0] == 0x45:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))

                self.tx_ds.normal['Vsens'] = ((value[0]<<8)|value[1])/100
                self.tx_ds.normal['Isens'] = ((value[2]<<8)|value[3])/100
                self.tx_ds.normal['Tsens'] = ((value[4]<<8)|value[5])/100
                self.tx_ds.normal['ACdem'] = ((value[6]<<8)|value[7])/100
                print('tx normal = {}'.format(self.tx_ds.normal))

                self.tx_ds.result['DCin'] = (self.tx_ds.normal['Vsens'])
                self.tx_ds.result['Vcoil'] = (self.tx_ds.normal['ACdem'])
                self.tx_ds.result['Iin'] = (self.tx_ds.normal['Isens'])
                self.tx_ds.result['Ttxboard'] = (self.tx_ds.normal['Tsens'])
                print('tx result = {}'.format(self.tx_ds.result))

            elif local_data[0] == 0x46:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))
                stat = '{:b}'.format(value[0]).zfill(8) #+ '{:b}'.format(value[1]).zfill(8)
                #stat = stat[:-6]
                print('stat = [{}]'.format(stat))

                self.tx_ds.over['Vsens'] = int(stat[0])
                self.tx_ds.over['ACdem'] = int(stat[1])
                self.tx_ds.under['Vsens'] = int(stat[2])
                self.tx_ds.under['ACdem'] = int(stat[3])
                self.tx_ds.low['Isens'] = int(stat[4])
                self.tx_ds.over['Tsens'] = int(stat[5])
                self.tx_ds.under['Tsens'] = int(stat[6])

                print('tx over = {}'.format(self.tx_ds.over))
                print('tx under = {}'.format(self.tx_ds.under))
                print('tx low = {}'.format(self.tx_ds.low))

            elif local_data[0] == 0x47:
                value = local_data[2:-2]
                print('value = [{}]'.format(', '.join(hex(x) for x in value)))
                
                self.tx_ds.thd_over['Vsens'] = ((value[0]<<8)|value[1])/100
                self.tx_ds.thd_over['ACdem'] = ((value[2]<<8)|value[3])/100
                self.tx_ds.thd_under['Vsens'] = ((value[4]<<8)|value[5])/100
                self.tx_ds.thd_under['ACdem'] = ((value[6]<<8)|value[7])/100
                self.tx_ds.thd_low['Isens'] = ((value[8]<<8)|value[9])/100
                self.tx_ds.thd_over['Tsens'] = ((value[10]<<8)|value[11])/100
                self.tx_ds.thd_under['Tsens'] = ((value[12]<<8)|value[13])/100
                
                print('tx thd_over = {}'.format(self.tx_ds.thd_over))
                print('tx thd_over = {}'.format(self.tx_ds.thd_over))
                print('tx thd_low = {}'.format(self.tx_ds.thd_low))
                
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    form = exampleapp()
    form.show()

    timer = QTimer()
    timer.timeout.connect(form.tick)
    timer.start(1000)
    
    app.exec_()
    
    



