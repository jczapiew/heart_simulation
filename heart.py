from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import GUI.heartGUI as heartGUI
import sys

a, b, k0, k1 = 0.9, 0.25, 0.29, 0.2
th = 0.8
tce = k0 + k1 * th

class HeartSimulation(QMainWindow):
    def __init__(self):
        # inicjalizacja GUI
        super(HeartSimulation, self).__init__()
        self.gui = heartGUI.Ui_MainWindow()
        self.gui.setupUi(self)

        # inicjalizacja wszystkich potrzebnych parametrow stalych i zmiennych
        self.Vunlv, self.Vunla, self.Vunrv, self.Vunra, self.Emaxlv, self.Eminlv, self.Ela, self.Emaxrv, self.Eminrv,\
        self.Era, self.Rla, self.Rra, self.Llv, self.Lla, self.Lrv, self.Lra, self.Vuna1, self.Vuna2, self.Vuna3,\
        self.Vunv1, self.Vunv2, self.R0s, self.Ra1, self.Ra2, self.Ra3, self.Rv1, self.Rv2, self.Ca1, self.Ca2,\
        self.Ca3, self.Cv1, self.Cv2, self.La1, self.Lv2, self.Vunp1, self.Vunp2, self.Vunp3, self.Vunl1, self.Vunl2,\
        self.R0p, self.Rp1, self.Rp2, self.Rp3, self.Rl1, self.Rl2, self.Cp1, self.Cp2, self.Cp3, self.Cl1, self.Cl2,\
        self.Lp1, self.Ll2 = parameters_values()

        # Okres trwania jednego cyklu serca, 0.8 sekundy
        self.th = th

        self.Qla, self.Qlv, self.Qra, self.Qrv, self.Vla, self.Vlv, self.Vra, self.Vrv, self.Qa1, self.Qv2, self.Va1,\
        self.Va2, self.Va3, self.Vv1, self.Vv2, self.Qp1, self.Ql2, self.Vp1, self.Vp2, self.Vp3, self.Vl1,\
        self.Vl2 = starting_values()

        self.pla, self.plv, self.pas, self.fi, self.Elv, self.Erv, self.pra, self.prv, self.pap, self.pp1, self.Qp2,\
        self.pp2, self.Qp3, self.pp3, self.Ql1, self.pl1, self.pl2, self.pa1, self.Qa2, self.pa2, self.Qa3, self.pa3,\
        self.Qv1, self.pv1, self.pv2 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
                                       [], [], [], [], []
        self.sims_start = 0
        self.sims_end = 32
        self.sims_step = 0.0001

        if self.sims_end == self.th:
            self.fig_start = 0
        elif np.round(self.sims_end / self.th, decimals=3) % 1 == 0:
            self.fig_start = np.round((((self.sims_end // self.th) + 1) * self.th) - self.th, decimals=3)
        else:
            self.fig_start = np.round(((self.sims_end // self.th) * self.th) - self.th, decimals=3)
        if self.fig_start == self.sims_end:
            self.fig_start -= self.th

        self.string_to_print = ""

        # obsluga GUI
        self.gui.simulationTimeLineEdit.setText(str(self.sims_end))
        self.gui.lineEdit_th.setText(str(th))
        self.gui.simulationButton.clicked.connect(self.run_simulation)
        self.gui.fullSimulationButton.clicked.connect(self.plot_prepared_simulation)
        self.gui.simulationTimeLineEdit.textChanged.connect(self.change_sim_end)
        self.gui.pushButton_increase.clicked.connect(self.increase_resistances)
        self.gui.pushButton_return.clicked.connect(self.return_to_normal_resistances)
        self.gui.lineEdit_th.textChanged.connect(self.change_th)

    def increase_resistances(self):
        if self.Ra2 < 0.7:
            self.Ra1 *= 2
            self.Ra2 *= 2
            self.Rp1 *= 2
            self.Rp2 *= 2
            print_it = ""
            print_it += "Wartość Ra1: " + str(self.Ra1) + " (mmHg * s)/ml\n"
            print_it += "Wartość Ra2: " + str(self.Ra2) + " (mmHg * s)/ml\n"
            print_it += "Wartość Rp1: " + str(self.Rp1) + " (mmHg * s)/ml\n"
            print_it += "Wartość Rp2: " + str(self.Rp2) + " (mmHg * s)/ml\n"
            self.gui.textEdit.setText(print_it)
        else:
            self.gui.textEdit.setText("Zbyt duża wartość rezystancji tętnic.")

    def return_to_normal_resistances(self):
        self.Ra1 = 0.0824
        self.Ra2 = 0.178
        self.Rp1 = 0.0227
        self.Rp2 = 0.053
        print_it = ""
        print_it += "Przywrócono domyślne wartości rezystancji.\n\n"
        print_it += "Wartość Ra1: " + str(self.Ra1) + " (mmHg * s)/ml\n"
        print_it += "Wartość Ra2: " + str(self.Ra2) + " (mmHg * s)/ml\n"
        print_it += "Wartość Rp1: " + str(self.Rp1) + " (mmHg * s)/ml\n"
        print_it += "Wartość Rp2: " + str(self.Rp2) + " (mmHg * s)/ml\n"
        self.gui.textEdit.setText(print_it)

    def change_th(self):
        global th, tce
        try:
            if float(self.gui.lineEdit_th.text()) == 0.6:
                self.gui.textEdit.setText("")
                th = 0.6
                self.th = 0.6
            elif float(self.gui.lineEdit_th.text()) == 0.7:
                self.gui.textEdit.setText("")
                th = 0.7
                self.th = 0.7
            elif float(self.gui.lineEdit_th.text()) == 0.8:
                self.gui.textEdit.setText("")
                th = 0.8
                self.th = 0.8
            elif float(self.gui.lineEdit_th.text()) == 0.9:
                self.gui.textEdit.setText("")
                th = 0.9
                self.th = 0.9
            elif float(self.gui.lineEdit_th.text()) == 1.0:
                self.gui.textEdit.setText("")
                th = 1.0
                self.th = 1.0
            else:
                printer = ""
                printer += "Wartość długości cyklu pracy serca niedozwolona!\n"
                printer += "Wybierz wartość ze zbioru {0.6, 0.7, 0.8, 0.9, 1.0}."
                self.gui.textEdit.setText(printer)
            tce = k0 + k1 * th
        except ValueError:
            self.gui.textEdit.setText("Zła wartość długości cyklu pracy serca!")

    def change_sim_end(self):
        try:
            if float(self.gui.simulationTimeLineEdit.text()) >= self.th and float(self.gui.simulationTimeLineEdit.text()) < 80:
                self.gui.textEdit.setText("")
                self.sims_end = float(self.gui.simulationTimeLineEdit.text())
            else:
                printer = ""
                printer += "Wartość długości symulacji spoza zakresu!\n"
                printer += "Wybierz wartość długości symulacji z zakresu <" + str(self.th) + ", 80>."
                self.gui.textEdit.setText(printer)
        except ValueError:
            self.gui.textEdit.setText("Zła wartość długości symulacji!")

    def run_simulation(self):
        self.string_to_print = ""

        if self.sims_end == self.th:
            self.fig_start = 0
        elif np.round(self.sims_end / self.th, decimals=3) % 1 == 0:
            self.fig_start = np.round((((self.sims_end // self.th) + 1) * self.th) - self.th, decimals=3)
        else:
            self.fig_start = np.round(((self.sims_end // self.th) * self.th) - self.th, decimals=3)
        if self.fig_start == self.sims_end:
            self.fig_start -= self.th

        h = self.sims_step
        time = np.arange(self.sims_start, self.sims_end + h, h)

        print("Początek charakterystyki: ", self.fig_start, "s")
        print("Długość symulacji: ", self.sims_end, "s")
        print("Krok algorytmu: ", self.sims_step, "s")
        print("Wartość th: ", self.th, "s")

        self.Qla, self.Qlv, self.Qra, self.Qrv, self.Vla, self.Vlv, self.Vra, self.Vrv, self.Qa1, self.Qv2, self.Va1, \
        self.Va2, self.Va3, self.Vv1, self.Vv2, self.Qp1, self.Ql2, self.Vp1, self.Vp2, self.Vp3, self.Vl1, \
        self.Vl2 = starting_values()

        self.pla, self.plv, self.pas, self.fi, self.Elv, self.Erv, self.pra, self.prv, self.pap, self.pp1, self.Qp2, \
        self.pp2, self.Qp3, self.pp3, self.Ql1, self.pl1, self.pl2, self.pa1, self.Qa2, self.pa2, self.Qa3, self.pa3, \
        self.Qv1, self.pv1, self.pv2 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
                                       [], [], [], [], []

        valves = [False, False, False, False]

        time1 = datetime.now()
        for i in range(len(time) - 1):
            t = time[i]

            '''
            Obliczanie wartosci rownan standardowych z zaleznosci liniowych oraz obliczanie wartości równań
            różniczkowych w kolejnym kroku metodą Rungego-Kutty czwartego rzędu
            '''

            # Obliczanie fi oraz elastancji
            self.fi.append(fi_fun(t))
            self.Elv.append(elastance_fun(t, self.Eminlv, self.Emaxlv))
            self.Erv.append(elastance_fun(t, self.Eminrv, self.Emaxrv))

            # Cisnienia i przeplywy w krwiobiegu malym
            self.pp1.append(pressure_fun3(self.Vp1[i], self.Vunp1, self.Cp1))
            self.pp2.append(pressure_fun3(self.Vp2[i], self.Vunp2, self.Cp2))
            self.pp3.append(pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3))
            self.pl1.append(pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1))
            self.pl2.append(pressure_fun3(self.Vl2[i], self.Vunl2, self.Cl2))
            self.Qp2.append(blood_flow_fun(self.pp2[i], self.pp3[i], self.Rp2, 0, 0))
            self.Qp3.append(blood_flow_fun(self.pp3[i], self.pl1[i], self.Rp3, 0, 0))
            self.Ql1.append(blood_flow_fun(self.pl1[i], self.pl2[i], self.Rl1, 0, 0))

            # Cisnienia i przeplywy w krwiobiegu duzym
            self.pa1.append(pressure_fun3(self.Va1[i], self.Vuna1, self.Ca1))
            self.pa2.append(pressure_fun3(self.Va2[i], self.Vuna2, self.Ca2))
            self.pa3.append(pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3))
            self.pv1.append(pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1))
            self.pv2.append(pressure_fun3(self.Vv2[i], self.Vunv2, self.Cv2))
            self.Qa2.append(blood_flow_fun(self.pa2[i], self.pa3[i], self.Ra2, 0, 0))
            self.Qa3.append(blood_flow_fun(self.pa3[i], self.pv1[i], self.Ra3, 0, 0))
            self.Qv1.append(blood_flow_fun(self.pv1[i], self.pv2[i], self.Rv1, 0, 0))

            # Cisnienia w komorach serca
            self.pla.append(pressure_fun1(self.Ela, self.Vla[i], self.Vunla))
            self.plv.append(pressure_fun1(elastance_fun(t, self.Eminlv, self.Emaxlv), self.Vlv[i], self.Vunlv))
            self.pas.append(pressure_fun2(self.R0s, self.Qlv[i], self.pa1[i]))
            self.pra.append(pressure_fun1(self.Era, self.Vra[i], self.Vunra))
            self.prv.append(pressure_fun1(elastance_fun(t, self.Eminrv, self.Emaxrv), self.Vrv[i], self.Vunrv))
            self.pap.append(pressure_fun2(self.R0p, self.Qrv[i], self.pp1[i]))

            '''
            Otwieranie i zamykanie zastawek
            '''

            if self.pla[i] > self.plv[i] and valves[0] is False:
                valves[0] = True
            elif self.pla[i] < self.plv[i] and valves[0] is True and self.Qla[i] < 0:
                valves[0] = False

            if self.plv[i] > self.pas[i] and valves[1] is False:
                valves[1] = True
            elif self.plv[i] < self.pas[i] and valves[1] is True and self.Qlv[i] < 0:
                valves[1] = False

            if self.pra[i] > self.prv[i] and valves[2] is False:
                valves[2] = True
            elif self.pra[i] < self.prv[i] and valves[2] is True and self.Qra[i] < 0:
                valves[2] = False

            if self.prv[i] > self.pap[i] and valves[3] is False:
                valves[3] = True
            elif self.prv[i] < self.pap[i] and valves[3] is True and self.Qrv[i] < 0:
                valves[3] = False

            '''
            Wspolczynniki do metody Rungego-Kutty
            '''

            # Wspolczynniki k1
            if valves[0] is True:
                k1qla = blood_flow_fun(pressure_fun1(self.Ela, self.Vla[i], self.Vunla),
                                       pressure_fun1(elastance_fun(t, self.Eminlv, self.Emaxlv), self.Vlv[i],
                                                     self.Vunlv),
                                       self.Lla, self.Rla, self.Qla[i])
            else:
                k1qla = 0
            if valves[1] is True:
                k1qlv = blood_flow_fun(pressure_fun1(elastance_fun(t, self.Eminlv, self.Emaxlv), self.Vlv[i],
                                                     self.Vunlv),
                                       pressure_fun2(self.R0s, self.Qlv[i],
                                                     pressure_fun3(self.Va1[i], self.Vuna1, self.Ca1)),
                                       self.Llv, 0, 0)
            else:
                k1qlv = 0
            if valves[2] is True:
                k1qra = blood_flow_fun(pressure_fun1(self.Era, self.Vra[i], self.Vunra),
                                       pressure_fun1(elastance_fun(t, self.Eminrv, self.Emaxrv), self.Vrv[i],
                                                     self.Vunrv),
                                       self.Lra, self.Rra, self.Qra[i])
            else:
                k1qra = 0
            if valves[3] is True:
                k1qrv = blood_flow_fun(pressure_fun1(elastance_fun(t, self.Eminrv, self.Emaxrv), self.Vrv[i],
                                                     self.Vunrv),
                                       pressure_fun2(self.R0p, self.Qrv[i],
                                                     pressure_fun3(self.Vp1[i], self.Vunp1, self.Cp1)),
                                       self.Lrv, 0, 0)
            else:
                k1qrv = 0
            k1vla = volume_fun(self.Ql2[i], self.Qla[i])
            k1vlv = volume_fun(self.Qla[i], self.Qlv[i])
            k1vra = volume_fun(self.Qv2[i], self.Qra[i])
            k1vrv = volume_fun(self.Qra[i], self.Qrv[i])

            k1qp1 = blood_flow_fun(pressure_fun3(self.Vp1[i], self.Vunp1, self.Cp1),
                                   pressure_fun3(self.Vp2[i], self.Vunp2, self.Cp2),
                                   self.Lp1, self.Rp1, self.Qp1[i])
            k1vp1 = volume_fun(self.Qrv[i], self.Qp1[i])
            k1vp2 = volume_fun(self.Qp1[i], blood_flow_fun(pressure_fun3(self.Vp2[i], self.Vunp2, self.Cp2),
                                                           pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3),
                                                           self.Rp2, 0, 0))
            k1vp3 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp2[i], self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0))
            k1vl1 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i], self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0))
            k1ql2 = blood_flow_fun(pressure_fun3(self.Vl2[i], self.Vunl2, self.Cl2),
                                   pressure_fun1(self.Ela, self.Vla[i], self.Vunla),
                                   self.Ll2, self.Rl2, self.Ql2[i])
            k1vl2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i], self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0), self.Ql2[i])

            k1qa1 = blood_flow_fun(pressure_fun3(self.Va1[i], self.Vuna1, self.Ca1),
                                   pressure_fun3(self.Va2[i], self.Vuna2, self.Ca2),
                                   self.La1, self.Ra1, self.Qa1[i])
            k1va1 = volume_fun(self.Qlv[i], self.Qa1[i])
            k1va2 = volume_fun(self.Qa1[i], blood_flow_fun(pressure_fun3(self.Va2[i], self.Vuna2, self.Ca2),
                                                           pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3),
                                                           self.Ra2, 0, 0))
            k1va3 = volume_fun(blood_flow_fun(pressure_fun3(self.Va2[i], self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0))
            k1vv1 = volume_fun(blood_flow_fun(pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i], self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0))
            k1qv2 = blood_flow_fun(pressure_fun3(self.Vv2[i], self.Vunv2, self.Cv2),
                                   pressure_fun1(self.Era, self.Vra[i], self.Vunra),
                                   self.Lv2, self.Rv2, self.Qv2[i])
            k1vv2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i], self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0), self.Qv2[i])

            # Wspolczynniki k2
            if valves[0] is True:
                k2qla = blood_flow_fun(pressure_fun1(self.Ela, self.Vla[i] + (k1vla * h) / 2, self.Vunla),
                                       pressure_fun1(elastance_fun(t + h / 2, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k1vlv * h) / 2, self.Vunlv),
                                       self.Lla, self.Rla, self.Qla[i] + (k1qla * h) / 2)
            else:
                k2qla = 0
            if valves[1] is True:
                k2qlv = blood_flow_fun(pressure_fun1(elastance_fun(t + h / 2, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k1vlv * h) / 2, self.Vunlv),
                                       pressure_fun2(self.R0s, self.Qlv[i] + (k1qlv * h) / 2,
                                                     pressure_fun3(self.Va1[i] + (k1va1 * h) / 2, self.Vuna1,
                                                                   self.Ca1)),
                                       self.Llv, 0, 0)
            else:
                k2qlv = 0
            if valves[2] is True:
                k2qra = blood_flow_fun(pressure_fun1(self.Era, self.Vra[i] + (k1vra * h) / 2, self.Vunra),
                                       pressure_fun1(elastance_fun(t + h / 2, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k1vrv * h) / 2, self.Vunrv),
                                       self.Lra, self.Rra, self.Qra[i] + (k1qra * h) / 2)
            else:
                k2qra = 0
            if valves[3] is True:
                k2qrv = blood_flow_fun(pressure_fun1(elastance_fun(t + h / 2, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k1vrv * h) / 2, self.Vunrv),
                                       pressure_fun2(self.R0p, self.Qrv[i] + (k1qrv * h) / 2,
                                                     pressure_fun3(self.Vp1[i] + (k1vp1 * h) / 2, self.Vunp1,
                                                                   self.Cp1)),
                                       self.Lrv, 0, 0)
            else:
                k2qrv = 0
            k2vla = volume_fun(self.Ql2[i] + (k1ql2 * h) / 2, self.Qla[i] + (k1qla * h) / 2)
            k2vlv = volume_fun(self.Qla[i] + (k1qla * h) / 2, self.Qlv[i] + (k1qlv * h) / 2)
            k2vra = volume_fun(self.Qv2[i] + (k1qv2 * h) / 2, self.Qra[i] + (k1qra * h) / 2)
            k2vrv = volume_fun(self.Qra[i] + (k1qra * h) / 2, self.Qrv[i] + (k1qrv * h) / 2)

            k2qp1 = blood_flow_fun(pressure_fun3(self.Vp1[i] + (k1vp1 * h) / 2, self.Vunp1, self.Cp1),
                                   pressure_fun3(self.Vp2[i] + (k1vp2 * h) / 2, self.Vunp2, self.Cp2),
                                   self.Lp1, self.Rp1, self.Qp1[i] + (k1qp1 * h) / 2)
            k2vp1 = volume_fun(self.Qrv[i] + (k1qrv * h) / 2, self.Qp1[i] + (k1qp1 * h) / 2)
            k2vp2 = volume_fun(self.Qp1[i] + (k1qp1 * h) / 2,
                               blood_flow_fun(pressure_fun3(self.Vp2[i] + (k1vp2 * h) / 2, self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k1vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0))
            k2vp3 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp2[i] + (k1vp2 * h) / 2, self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k1vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vp3[i] + (k1vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k1vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0))
            k2vl1 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp3[i] + (k1vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k1vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vl1[i] + (k1vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k1vl2 * h) / 2, self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0))
            k2ql2 = blood_flow_fun(pressure_fun3(self.Vl2[i] + (k1vl2 * h) / 2, self.Vunl2, self.Cl2),
                                   pressure_fun1(self.Ela, self.Vla[i] + (k1vla * h) / 2, self.Vunla),
                                   self.Ll2, self.Rl2, self.Ql2[i] + (k1ql2 * h) / 2)
            k2vl2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vl1[i] + (k1vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k1vl2 * h) / 2, self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0), self.Ql2[i] + (k1ql2 * h) / 2)

            k2qa1 = blood_flow_fun(pressure_fun3(self.Va1[i] + (k1va1 * h) / 2, self.Vuna1, self.Ca1),
                                   pressure_fun3(self.Va2[i] + (k1va2 * h) / 2, self.Vuna2, self.Ca2),
                                   self.La1, self.Ra1, self.Qa1[i] + (k1qa1 * h) / 2)
            k2va1 = volume_fun(self.Qlv[i] + (k1qlv * h) / 2, self.Qa1[i] + (k1qa1 * h) / 2)
            k2va2 = volume_fun(self.Qa1[i] + (k1qa1 * h) / 2,
                               blood_flow_fun(pressure_fun3(self.Va2[i] + (k1va2 * h) / 2, self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k1va3 * h) / 2, self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0))
            k2va3 = volume_fun(blood_flow_fun(pressure_fun3(self.Va2[i] + (k1va2 * h) / 2, self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k1va3 * h) / 2, self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Va3[i] + (k1va3 * h) / 2, self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k1vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0))
            k2vv1 = volume_fun(blood_flow_fun(pressure_fun3(self.Va3[i] + (k1va3 * h) / 2, self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k1vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vv1[i] + (k1vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k1vv2 * h) / 2, self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0))
            k2qv2 = blood_flow_fun(pressure_fun3(self.Vv2[i] + (k1vv2 * h) / 2, self.Vunv2, self.Cv2),
                                   pressure_fun1(self.Era, self.Vra[i] + (k1vra * h) / 2, self.Vunra),
                                   self.Lv2, self.Rv2, self.Qv2[i] + (k1qv2 * h) / 2)
            k2vv2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vv1[i] + (k1vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k1vv2 * h) / 2, self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0), self.Qv2[i] + (k1qv2 * h) / 2)

            # Wspolczynniki k3
            if valves[0] is True:
                k3qla = blood_flow_fun(pressure_fun1(self.Ela, self.Vla[i] + (k2vla * h) / 2, self.Vunla),
                                       pressure_fun1(elastance_fun(t + h / 2, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k2vlv * h) / 2, self.Vunlv),
                                       self.Lla, self.Rla, self.Qla[i] + (k2qla * h) / 2)
            else:
                k3qla = 0
            if valves[1] is True:
                k3qlv = blood_flow_fun(pressure_fun1(elastance_fun(t + h / 2, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k2vlv * h) / 2, self.Vunlv),
                                       pressure_fun2(self.R0s, self.Qlv[i] + (k2qlv * h) / 2,
                                                     pressure_fun3(self.Va1[i] + (k2va1 * h) / 2, self.Vuna1,
                                                                   self.Ca1)),
                                       self.Llv, 0, 0)
            else:
                k3qlv = 0
            if valves[2] is True:
                k3qra = blood_flow_fun(pressure_fun1(self.Era, self.Vra[i] + (k2vra * h) / 2, self.Vunra),
                                       pressure_fun1(elastance_fun(t + h / 2, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k2vrv * h) / 2, self.Vunrv),
                                       self.Lra, self.Rra, self.Qra[i] + (k2qra * h) / 2)
            else:
                k3qra = 0
            if valves[3] is True:
                k3qrv = blood_flow_fun(pressure_fun1(elastance_fun(t + h / 2, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k2vrv * h) / 2, self.Vunrv),
                                       pressure_fun2(self.R0p, self.Qrv[i] + (k2qrv * h) / 2,
                                                     pressure_fun3(self.Vp1[i] + (k2vp1 * h) / 2, self.Vunp1,
                                                                   self.Cp1)),
                                       self.Lrv, 0, 0)
            else:
                k3qrv = 0
            k3vla = volume_fun(self.Ql2[i] + (k2ql2 * h) / 2, self.Qla[i] + (k2qla * h) / 2)
            k3vlv = volume_fun(self.Qla[i] + (k2qla * h) / 2, self.Qlv[i] + (k2qlv * h) / 2)
            k3vra = volume_fun(self.Qv2[i] + (k2qv2 * h) / 2, self.Qra[i] + (k2qra * h) / 2)
            k3vrv = volume_fun(self.Qra[i] + (k2qra * h) / 2, self.Qrv[i] + (k2qrv * h) / 2)

            k3qp1 = blood_flow_fun(pressure_fun3(self.Vp1[i] + (k2vp1 * h) / 2, self.Vunp1, self.Cp1),
                                   pressure_fun3(self.Vp2[i] + (k2vp2 * h) / 2, self.Vunp2, self.Cp2),
                                   self.Lp1, self.Rp1, self.Qp1[i] + (k2qp1 * h) / 2)
            k3vp1 = volume_fun(self.Qrv[i] + (k2qrv * h) / 2, self.Qp1[i] + (k2qp1 * h) / 2)
            k3vp2 = volume_fun(self.Qp1[i] + (k2qp1 * h) / 2,
                               blood_flow_fun(pressure_fun3(self.Vp2[i] + (k2vp2 * h) / 2, self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k2vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0))
            k3vp3 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp2[i] + (k2vp2 * h) / 2, self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k2vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vp3[i] + (k2vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k2vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0))
            k3vl1 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp3[i] + (k2vp3 * h) / 2, self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k2vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vl1[i] + (k2vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k2vl2 * h) / 2, self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0))
            k3ql2 = blood_flow_fun(pressure_fun3(self.Vl2[i] + (k2vl2 * h) / 2, self.Vunl2, self.Cl2),
                                   pressure_fun1(self.Ela, self.Vla[i] + (k2vla * h) / 2, self.Vunla),
                                   self.Ll2, self.Rl2, self.Ql2[i] + (k2ql2 * h) / 2)
            k3vl2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vl1[i] + (k2vl1 * h) / 2, self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k2vl2 * h) / 2, self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0), self.Ql2[i] + (k2ql2 * h) / 2)

            k3qa1 = blood_flow_fun(pressure_fun3(self.Va1[i] + (k2va1 * h) / 2, self.Vuna1, self.Ca1),
                                   pressure_fun3(self.Va2[i] + (k2va2 * h) / 2, self.Vuna2, self.Ca2),
                                   self.La1, self.Ra1, self.Qa1[i] + (k2qa1 * h) / 2)
            k3va1 = volume_fun(self.Qlv[i] + (k2qlv * h) / 2, self.Qa1[i] + (k2qa1 * h) / 2)
            k3va2 = volume_fun(self.Qa1[i] + (k2qa1 * h) / 2,
                               blood_flow_fun(pressure_fun3(self.Va2[i] + (k2va2 * h) / 2, self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k2va3 * h) / 2, self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0))
            k3va3 = volume_fun(blood_flow_fun(pressure_fun3(self.Va2[i] + (k2va2 * h) / 2, self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k2va3 * h) / 2, self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Va3[i] + (k2va3 * h) / 2, self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k2vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0))
            k3vv1 = volume_fun(blood_flow_fun(pressure_fun3(self.Va3[i] + (k2va3 * h) / 2, self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k2vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vv1[i] + (k2vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k2vv2 * h) / 2, self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0))
            k3qv2 = blood_flow_fun(pressure_fun3(self.Vv2[i] + (k2vv2 * h) / 2, self.Vunv2, self.Cv2),
                                   pressure_fun1(self.Era, self.Vra[i] + (k2vra * h) / 2, self.Vunra),
                                   self.Lv2, self.Rv2, self.Qv2[i] + (k2qv2 * h) / 2)
            k3vv2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vv1[i] + (k2vv1 * h) / 2, self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k2vv2 * h) / 2, self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0), self.Qv2[i] + (k2qv2 * h) / 2)

            # Wspolczynniki k4
            if valves[0] is True:
                k4qla = blood_flow_fun(pressure_fun1(self.Ela, self.Vla[i] + (k3vla * h), self.Vunla),
                                       pressure_fun1(elastance_fun(t + h, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k3vlv * h), self.Vunlv),
                                       self.Lla, self.Rla, self.Qla[i] + (k3qla * h))
            else:
                k4qla = 0
            if valves[1] is True:
                k4qlv = blood_flow_fun(pressure_fun1(elastance_fun(t + h, self.Eminlv, self.Emaxlv),
                                                     self.Vlv[i] + (k3vlv * h), self.Vunlv),
                                       pressure_fun2(self.R0s, self.Qlv[i] + (k3qlv * h),
                                                     pressure_fun3(self.Va1[i] + (k3va1 * h), self.Vuna1,
                                                                   self.Ca1)),
                                       self.Llv, 0, 0)
            else:
                k4qlv = 0
            if valves[2] is True:
                k4qra = blood_flow_fun(pressure_fun1(self.Era, self.Vra[i] + (k3vra * h), self.Vunra),
                                       pressure_fun1(elastance_fun(t + h, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k3vrv * h), self.Vunrv),
                                       self.Lra, self.Rra, self.Qra[i] + (k3qra * h))
            else:
                k4qra = 0
            if valves[3] is True:
                k4qrv = blood_flow_fun(pressure_fun1(elastance_fun(t + h, self.Eminrv, self.Emaxrv),
                                                     self.Vrv[i] + (k3vrv * h), self.Vunrv),
                                       pressure_fun2(self.R0p, self.Qrv[i] + (k3qrv * h),
                                                     pressure_fun3(self.Vp1[i] + (k3vp1 * h), self.Vunp1,
                                                                   self.Cp1)),
                                       self.Lrv, 0, 0)
            else:
                k4qrv = 0
            k4vla = volume_fun(self.Ql2[i] + (k3ql2 * h), self.Qla[i] + (k3qla * h))
            k4vlv = volume_fun(self.Qla[i] + (k3qla * h), self.Qlv[i] + (k3qlv * h))
            k4vra = volume_fun(self.Qv2[i] + (k3qv2 * h), self.Qra[i] + (k3qra * h))
            k4vrv = volume_fun(self.Qra[i] + (k3qra * h), self.Qrv[i] + (k3qrv * h))

            k4qp1 = blood_flow_fun(pressure_fun3(self.Vp1[i] + (k3vp1 * h), self.Vunp1, self.Cp1),
                                   pressure_fun3(self.Vp2[i] + (k3vp2 * h), self.Vunp2, self.Cp2),
                                   self.Lp1, self.Rp1, self.Qp1[i] + (k3qp1 * h))
            k4vp1 = volume_fun(self.Qrv[i] + (k3qrv * h), self.Qp1[i] + (k3qp1 * h))
            k4vp2 = volume_fun(self.Qp1[i] + (k3qp1 * h),
                               blood_flow_fun(pressure_fun3(self.Vp2[i] + (k3vp2 * h), self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k3vp3 * h), self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0))
            k4vp3 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp2[i] + (k3vp2 * h), self.Vunp2, self.Cp2),
                                              pressure_fun3(self.Vp3[i] + (k3vp3 * h), self.Vunp3, self.Cp3),
                                              self.Rp2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vp3[i] + (k3vp3 * h), self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k3vl1 * h), self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0))
            k4vl1 = volume_fun(blood_flow_fun(pressure_fun3(self.Vp3[i] + (k3vp3 * h), self.Vunp3, self.Cp3),
                                              pressure_fun3(self.Vl1[i] + (k3vl1 * h), self.Vunl1, self.Cl1),
                                              self.Rp3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vl1[i] + (k3vl1 * h), self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k3vl2 * h), self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0))
            k4ql2 = blood_flow_fun(pressure_fun3(self.Vl2[i] + (k3vl2 * h), self.Vunl2, self.Cl2),
                                   pressure_fun1(self.Ela, self.Vla[i] + (k3vla * h), self.Vunla),
                                   self.Ll2, self.Rl2, self.Ql2[i] + (k3ql2 * h))
            k4vl2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vl1[i] + (k3vl1 * h), self.Vunl1, self.Cl1),
                                              pressure_fun3(self.Vl2[i] + (k3vl2 * h), self.Vunl2, self.Cl2),
                                              self.Rl1, 0, 0), self.Ql2[i] + (k3ql2 * h))

            k4qa1 = blood_flow_fun(pressure_fun3(self.Va1[i] + (k3va1 * h), self.Vuna1, self.Ca1),
                                   pressure_fun3(self.Va2[i] + (k3va2 * h), self.Vuna2, self.Ca2),
                                   self.La1, self.Ra1, self.Qa1[i] + (k3qa1 * h))
            k4va1 = volume_fun(self.Qlv[i] + (k3qlv * h), self.Qa1[i] + (k3qa1 * h))
            k4va2 = volume_fun(self.Qa1[i] + (k3qa1 * h),
                               blood_flow_fun(pressure_fun3(self.Va2[i] + (k3va2 * h), self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k3va3 * h), self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0))
            k4va3 = volume_fun(blood_flow_fun(pressure_fun3(self.Va2[i] + (k3va2 * h), self.Vuna2, self.Ca2),
                                              pressure_fun3(self.Va3[i] + (k3va3 * h), self.Vuna3, self.Ca3),
                                              self.Ra2, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Va3[i] + (k3va3 * h), self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k3vv1 * h), self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0))
            k4vv1 = volume_fun(blood_flow_fun(pressure_fun3(self.Va3[i] + (k3va3 * h), self.Vuna3, self.Ca3),
                                              pressure_fun3(self.Vv1[i] + (k3vv1 * h), self.Vunv1, self.Cv1),
                                              self.Ra3, 0, 0),
                               blood_flow_fun(pressure_fun3(self.Vv1[i] + (k3vv1 * h), self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k3vv2 * h), self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0))
            k4qv2 = blood_flow_fun(pressure_fun3(self.Vv2[i] + (k3vv2 * h), self.Vunv2, self.Cv2),
                                   pressure_fun1(self.Era, self.Vra[i] + (k3vra * h), self.Vunra),
                                   self.Lv2, self.Rv2, self.Qv2[i] + (k3qv2 * h))
            k4vv2 = volume_fun(blood_flow_fun(pressure_fun3(self.Vv1[i] + (k3vv1 * h), self.Vunv1, self.Cv1),
                                              pressure_fun3(self.Vv2[i] + (k3vv2 * h), self.Vunv2, self.Cv2),
                                              self.Rv1, 0, 0), self.Qv2[i] + (k3qv2 * h))

            # Obliczanie rownan rozniczkowych ze wspolczynnikow metody Rungego-Kutty 4 rzedu
            if valves[0] is True:
                self.Qla.append(self.Qla[i] + (1 / 6) * (k1qla + 2 * k2qla + 2 * k3qla + k4qla) * h)
            else:
                self.Qla.append(0)
            if valves[1] is True:
                self.Qlv.append(self.Qlv[i] + (1 / 6) * (k1qlv + 2 * k2qlv + 2 * k3qlv + k4qlv) * h)
            else:
                self.Qlv.append(0)
            if valves[2] is True:
                self.Qra.append(self.Qra[i] + (1 / 6) * (k1qra + 2 * k2qra + 2 * k3qra + k4qra) * h)
            else:
                self.Qra.append(0)
            if valves[3] is True:
                self.Qrv.append(self.Qrv[i] + (1 / 6) * (k1qrv + 2 * k2qrv + 2 * k3qrv + k4qrv) * h)
            else:
                self.Qrv.append(0)
            self.Vla.append(self.Vla[i] + (1 / 6) * (k1vla + 2 * k2vla + 2 * k3vla + k4vla) * h)
            self.Vlv.append(self.Vlv[i] + (1 / 6) * (k1vlv + 2 * k2vlv + 2 * k3vlv + k4vlv) * h)
            self.Vra.append(self.Vra[i] + (1 / 6) * (k1vra + 2 * k2vra + 2 * k3vra + k4vra) * h)
            self.Vrv.append(self.Vrv[i] + (1 / 6) * (k1vrv + 2 * k2vrv + 2 * k3vrv + k4vrv) * h)
            self.Qp1.append(self.Qp1[i] + (1 / 6) * (k1qp1 + 2 * k2qp1 + 2 * k3qp1 + k4qp1) * h)
            self.Ql2.append(self.Ql2[i] + (1 / 6) * (k1ql2 + 2 * k2ql2 + 2 * k3ql2 + k4ql2) * h)
            self.Vp1.append(self.Vp1[i] + (1 / 6) * (k1vp1 + 2 * k2vp1 + 2 * k3vp1 + k4vp1) * h)
            self.Vp2.append(self.Vp2[i] + (1 / 6) * (k1vp2 + 2 * k2vp2 + 2 * k3vp2 + k4vp2) * h)
            self.Vp3.append(self.Vp3[i] + (1 / 6) * (k1vp3 + 2 * k2vp3 + 2 * k3vp3 + k4vp3) * h)
            self.Vl1.append(self.Vl1[i] + (1 / 6) * (k1vl1 + 2 * k2vl1 + 2 * k3vl1 + k4vl1) * h)
            self.Vl2.append(self.Vl2[i] + (1 / 6) * (k1vl2 + 2 * k2vl2 + 2 * k3vl2 + k4vl2) * h)
            self.Qa1.append(self.Qa1[i] + (1 / 6) * (k1qa1 + 2 * k2qa1 + 2 * k3qa1 + k4qa1) * h)
            self.Qv2.append(self.Qv2[i] + (1 / 6) * (k1qv2 + 2 * k2qv2 + 2 * k3qv2 + k4qv2) * h)
            self.Va1.append(self.Va1[i] + (1 / 6) * (k1va1 + 2 * k2va1 + 2 * k3va1 + k4va1) * h)
            self.Va2.append(self.Va2[i] + (1 / 6) * (k1va2 + 2 * k2va2 + 2 * k3va2 + k4va2) * h)
            self.Va3.append(self.Va3[i] + (1 / 6) * (k1va3 + 2 * k2va3 + 2 * k3va3 + k4va3) * h)
            self.Vv1.append(self.Vv1[i] + (1 / 6) * (k1vv1 + 2 * k2vv1 + 2 * k3vv1 + k4vv1) * h)
            self.Vv2.append(self.Vv2[i] + (1 / 6) * (k1vv2 + 2 * k2vv2 + 2 * k3vv2 + k4vv2) * h)

        '''
        Po wyjściu z pętli trzeba obliczyć jeszcze końcowe wartości równań zwykłych
        '''

        i = -1
        t = time[i]

        # Obliczanie fi oraz elastancji
        self.fi.append(fi_fun(t))
        self.Elv.append(elastance_fun(t, self.Eminlv, self.Emaxlv))
        self.Erv.append(elastance_fun(t, self.Eminrv, self.Emaxrv))

        # Cisnienia i przeplywy w krwiobiegu malym
        self.pp1.append(pressure_fun3(self.Vp1[i], self.Vunp1, self.Cp1))
        self.pp2.append(pressure_fun3(self.Vp2[i], self.Vunp2, self.Cp2))
        self.pp3.append(pressure_fun3(self.Vp3[i], self.Vunp3, self.Cp3))
        self.pl1.append(pressure_fun3(self.Vl1[i], self.Vunl1, self.Cl1))
        self.pl2.append(pressure_fun3(self.Vl2[i], self.Vunl2, self.Cl2))
        self.Qp2.append(blood_flow_fun(self.pp2[i], self.pp3[i], self.Rp2, 0, 0))
        self.Qp3.append(blood_flow_fun(self.pp3[i], self.pl1[i], self.Rp3, 0, 0))
        self.Ql1.append(blood_flow_fun(self.pl1[i], self.pl2[i], self.Rl1, 0, 0))

        # Cisnienia i przeplywy w krwiobiegu duzym
        self.pa1.append(pressure_fun3(self.Va1[i], self.Vuna1, self.Ca1))
        self.pa2.append(pressure_fun3(self.Va2[i], self.Vuna2, self.Ca2))
        self.pa3.append(pressure_fun3(self.Va3[i], self.Vuna3, self.Ca3))
        self.pv1.append(pressure_fun3(self.Vv1[i], self.Vunv1, self.Cv1))
        self.pv2.append(pressure_fun3(self.Vv2[i], self.Vunv2, self.Cv2))
        self.Qa2.append(blood_flow_fun(self.pa2[i], self.pa3[i], self.Ra2, 0, 0))
        self.Qa3.append(blood_flow_fun(self.pa3[i], self.pv1[i], self.Ra3, 0, 0))
        self.Qv1.append(blood_flow_fun(self.pv1[i], self.pv2[i], self.Rv1, 0, 0))

        # Cisnienia w komorach serca
        self.pla.append(pressure_fun1(self.Ela, self.Vla[i], self.Vunla))
        self.plv.append(pressure_fun1(elastance_fun(t, self.Eminlv, self.Emaxlv), self.Vlv[i], self.Vunlv))
        self.pas.append(pressure_fun2(self.R0s, self.Qlv[i], self.pa1[i]))
        self.pra.append(pressure_fun1(self.Era, self.Vra[i], self.Vunra))
        self.prv.append(pressure_fun1(elastance_fun(t, self.Eminrv, self.Emaxrv), self.Vrv[i], self.Vunrv))
        self.pap.append(pressure_fun2(self.R0p, self.Qrv[i], self.pp1[i]))

        time2 = datetime.now()

        data = np.zeros((15, len(self.Qla)) , dtype=np.float)

        data[0, :] = self.Qla
        data[1, :] = self.Qlv
        data[2, :] = self.Qra
        data[3, :] = self.Qrv
        data[4, :] = self.pla
        data[5, :] = self.plv
        data[6, :] = self.pas
        data[7, :] = self.pra
        data[8, :] = self.prv
        data[9, :] = self.pap
        data[10, :] = self.Vla
        data[11, :] = self.Vlv
        data[12, :] = self.Vra
        data[13, :] = self.Vrv
        data[14, 0] = self.sims_start
        data[14, 1] = self.sims_end
        data[14, 2] = self.sims_step

        if self.gui.saveFileCheckBox.isChecked() is True:
            f = open("data/data.txt", "w")
            np.savetxt(f, data)
            f.close()

        diff = time2 - time1
        self.string_to_print += "Długość symulowanego okresu: " + str(self.sims_end) + " s\n\n"
        self.string_to_print += "Czas trwania symulacji: " + str(np.round(diff.total_seconds(), decimals=3)) + " s\n\n"

        self.plot_results()

    def plot_prepared_simulation(self):
        self.string_to_print = ""

        try:
            data = np.loadtxt("data/data.txt")
        except OSError:
            self.gui.textEdit.setText("Nie znaleziono pliku z wartościami charakterystyk. Należy przeprowadzić najpierw"
                                      " pierwszą symulację.")
            return

        self.Qla = data[0, :]
        self.Qlv = data[1, :]
        self.Qra = data[2, :]
        self.Qrv = data[3, :]
        self.pla = data[4, :]
        self.plv = data[5, :]
        self.pas = data[6, :]
        self.pra = data[7, :]
        self.prv = data[8, :]
        self.pap = data[9, :]
        self.Vla = data[10, :]
        self.Vlv = data[11, :]
        self.Vra = data[12, :]
        self.Vrv = data[13, :]
        self.sims_start = data[14, 0]
        self.sims_end = data[14, 1]
        self.sims_step = data[14, 2]

        if self.sims_end == self.th:
            self.fig_start = 0
        elif np.round(self.sims_end / self.th, decimals=3) % 1 == 0:
            self.fig_start = np.round((((self.sims_end // self.th) + 1) * self.th) - self.th, decimals=3)
        else:
            self.fig_start = np.round(((self.sims_end // self.th) * self.th) - self.th, decimals=3)
        if self.fig_start == self.sims_end:
            self.fig_start -= self.th

        print("Początek charakterystyki: ", self.fig_start, "s")
        print("Długość symulacji: ", self.sims_end, "s")
        print("Krok algorytmu: ", self.sims_step, "s")

        self.string_to_print += "Długość symulowanego okresu: " + str(self.sims_end) + " s\n\n"

        self.string_to_print += "Wartości wczytano z pliku" + "\n\n"

        self.plot_results()

    def plot_results(self):
        time = np.arange(0, self.sims_end + self.sims_step, self.sims_step)
        time2 = np.arange(0, self.th, self.sims_step)

        time_diff = int(np.round(self.th / self.sims_step, decimals=3))
        fig_start = int(np.round(self.fig_start / self.sims_step, decimals=3))

        Qla = self.Qla[fig_start: fig_start + time_diff]
        Qlv = self.Qlv[fig_start: fig_start + time_diff]

        Qra = self.Qra[fig_start: fig_start + time_diff]
        Qrv = self.Qrv[fig_start: fig_start + time_diff]

        pla = self.pla[fig_start: fig_start + time_diff]
        plv = self.plv[fig_start: fig_start + time_diff]
        pas = self.pas[fig_start: fig_start + time_diff]

        pra = self.pra[fig_start: fig_start + time_diff]
        prv = self.prv[fig_start: fig_start + time_diff]
        pap = self.pap[fig_start: fig_start + time_diff]

        Vla = self.Vla[fig_start: fig_start + time_diff]
        Vlv = self.Vlv[fig_start: fig_start + time_diff]

        Vra = self.Vra[fig_start: fig_start + time_diff]
        Vrv = self.Vrv[fig_start: fig_start + time_diff]

        self.gui.leftBloodFlowWidget.canvas.ax.clear()
        self.gui.rightBloodFlowWidget.canvas.ax.clear()
        self.gui.leftPressuresWidget.canvas.ax.clear()
        self.gui.rightPressuresWidget.canvas.ax.clear()
        self.gui.leftVolumesWidget.canvas.ax.clear()
        self.gui.rightVolumesWidget.canvas.ax.clear()
        self.gui.pressuresVolumesWidget.canvas.ax.clear()

        if self.gui.fullSimulationCheckBox.isChecked() is False:
            self.gui.leftBloodFlowWidget.canvas.ax.plot(time2, Qla)
            self.gui.leftBloodFlowWidget.canvas.ax.plot(time2, Qlv)
            self.gui.leftBloodFlowWidget.canvas.ax.set_title("Przepływy krwi [ml/s]")
            self.gui.leftBloodFlowWidget.canvas.ax.legend(["Qla", "Qlv"])
            self.gui.leftBloodFlowWidget.canvas.draw()

            self.gui.rightBloodFlowWidget.canvas.ax.plot(time2, Qra)
            self.gui.rightBloodFlowWidget.canvas.ax.plot(time2, Qrv)
            self.gui.rightBloodFlowWidget.canvas.ax.set_title("Przepływy krwi [ml/s]")
            self.gui.rightBloodFlowWidget.canvas.ax.legend(["Qra", "Qrv"])
            self.gui.rightBloodFlowWidget.canvas.draw()

            self.gui.leftPressuresWidget.canvas.ax.plot(time2, pla)
            self.gui.leftPressuresWidget.canvas.ax.plot(time2, plv)
            self.gui.leftPressuresWidget.canvas.ax.plot(time2, pas)
            self.gui.leftPressuresWidget.canvas.ax.set_title("Ciśnienia naczyń [mmHg]")
            self.gui.leftPressuresWidget.canvas.ax.legend(["pla", "plv", "pas"])
            self.gui.leftPressuresWidget.canvas.draw()

            self.gui.rightPressuresWidget.canvas.ax.plot(time2, pra)
            self.gui.rightPressuresWidget.canvas.ax.plot(time2, prv)
            self.gui.rightPressuresWidget.canvas.ax.plot(time2, pap)
            self.gui.rightPressuresWidget.canvas.ax.set_title("Ciśnienia naczyń [mmHg]")
            self.gui.rightPressuresWidget.canvas.ax.legend(["pra", "prv", "pap"])
            self.gui.rightPressuresWidget.canvas.draw()

            self.gui.leftVolumesWidget.canvas.ax.plot(time2, Vla)
            self.gui.leftVolumesWidget.canvas.ax.plot(time2, Vlv)
            self.gui.leftVolumesWidget.canvas.ax.set_title("Objętości krwi [ml]")
            self.gui.leftVolumesWidget.canvas.ax.legend(["Vla", "Vlv"])
            self.gui.leftVolumesWidget.canvas.draw()

            self.gui.rightVolumesWidget.canvas.ax.plot(time2, Vra)
            self.gui.rightVolumesWidget.canvas.ax.plot(time2, Vrv)
            self.gui.rightVolumesWidget.canvas.ax.set_title("Objętości krwi [ml]")
            self.gui.rightVolumesWidget.canvas.ax.legend(["Vra", "Vrv"])
            self.gui.rightVolumesWidget.canvas.draw()

            self.gui.pressuresVolumesWidget.canvas.ax.plot(Vlv, plv)
            self.gui.pressuresVolumesWidget.canvas.ax.plot(Vrv, prv)
            self.gui.pressuresVolumesWidget.canvas.ax.set_title("p(V) [mmHg(ml)]")
            self.gui.pressuresVolumesWidget.canvas.ax.legend(["plv(Vlv)", "prv(Vrv)"])
            self.gui.pressuresVolumesWidget.canvas.draw()

            self.string_to_print += "Średnia wartość Qla: " + str(np.mean(Qla).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość Qlv: " + str(np.mean(Qlv).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość pla: " + str(np.mean(pla).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość plv: " + str(np.mean(plv).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość pas: " + str(np.mean(pas).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość Vla: " + str(np.mean(Vla).round(decimals=2)) + " [ml]\n"
            self.string_to_print += "Średnia wartość Vlv: " + str(np.mean(Vlv).round(decimals=2)) + " [ml]\n\n"

            self.string_to_print += "Średnia wartość Qra: " + str(np.mean(Qra).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość Qrv: " + str(np.mean(Qrv).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość pra: " + str(np.mean(pra).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość prv: " + str(np.mean(prv).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość pap: " + str(np.mean(pap).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość Vra: " + str(np.mean(Vra).round(decimals=2)) + " [ml]\n"
            self.string_to_print += "Średnia wartość Vrv: " + str(np.mean(Vrv).round(decimals=2)) + " [ml]\n"
        else:
            self.gui.leftBloodFlowWidget.canvas.ax.plot(time, self.Qla)
            self.gui.leftBloodFlowWidget.canvas.ax.plot(time, self.Qlv)
            self.gui.leftBloodFlowWidget.canvas.ax.set_title("Przepływy krwi [ml/s]")
            self.gui.leftBloodFlowWidget.canvas.ax.legend(["Qla", "Qlv"])
            self.gui.leftBloodFlowWidget.canvas.draw()

            self.gui.rightBloodFlowWidget.canvas.ax.plot(time, self.Qra)
            self.gui.rightBloodFlowWidget.canvas.ax.plot(time, self.Qrv)
            self.gui.rightBloodFlowWidget.canvas.ax.set_title("Przepływy krwi [ml/s]")
            self.gui.rightBloodFlowWidget.canvas.ax.legend(["Qra", "Qrv"])
            self.gui.rightBloodFlowWidget.canvas.draw()

            self.gui.leftPressuresWidget.canvas.ax.plot(time, self.pla)
            self.gui.leftPressuresWidget.canvas.ax.plot(time, self.plv)
            self.gui.leftPressuresWidget.canvas.ax.plot(time, self.pas)
            self.gui.leftPressuresWidget.canvas.ax.set_title("Ciśnienia naczyń [mmHg]")
            self.gui.leftPressuresWidget.canvas.ax.legend(["pla", "plv", "pas"])
            self.gui.leftPressuresWidget.canvas.draw()

            self.gui.rightPressuresWidget.canvas.ax.plot(time, self.pra)
            self.gui.rightPressuresWidget.canvas.ax.plot(time, self.prv)
            self.gui.rightPressuresWidget.canvas.ax.plot(time, self.pap)
            self.gui.rightPressuresWidget.canvas.ax.set_title("Ciśnienia naczyń [mmHg]")
            self.gui.rightPressuresWidget.canvas.ax.legend(["pra", "prv", "pap"])
            self.gui.rightPressuresWidget.canvas.draw()

            self.gui.leftVolumesWidget.canvas.ax.plot(time, self.Vla)
            self.gui.leftVolumesWidget.canvas.ax.plot(time, self.Vlv)
            self.gui.leftVolumesWidget.canvas.ax.set_title("Objętości krwi [ml]")
            self.gui.leftVolumesWidget.canvas.ax.legend(["Vla", "Vlv"])
            self.gui.leftVolumesWidget.canvas.draw()

            self.gui.rightVolumesWidget.canvas.ax.plot(time, self.Vra)
            self.gui.rightVolumesWidget.canvas.ax.plot(time, self.Vrv)
            self.gui.rightVolumesWidget.canvas.ax.set_title("Objętości krwi [ml]")
            self.gui.rightVolumesWidget.canvas.ax.legend(["Vra", "Vrv"])
            self.gui.rightVolumesWidget.canvas.draw()

            self.gui.pressuresVolumesWidget.canvas.ax.plot(self.Vlv, self.plv)
            self.gui.pressuresVolumesWidget.canvas.ax.plot(self.Vrv, self.prv)
            self.gui.pressuresVolumesWidget.canvas.ax.set_title("p(V) [mmHg(ml)]")
            self.gui.pressuresVolumesWidget.canvas.ax.legend(["plv(Vlv)", "prv(Vrv)"])
            self.gui.pressuresVolumesWidget.canvas.draw()

            self.string_to_print += "Średnia wartość Qla: " + str(np.mean(self.Qla).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość Qlv: " + str(np.mean(self.Qlv).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość pla: " + str(np.mean(self.pla).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość plv: " + str(np.mean(self.plv).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość pas: " + str(np.mean(self.pas).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość Vla: " + str(np.mean(self.Vla).round(decimals=2)) + " [ml]\n"
            self.string_to_print += "Średnia wartość Vlv: " + str(np.mean(self.Vlv).round(decimals=2)) + " [ml]\n\n"

            self.string_to_print += "Średnia wartość Qra: " + str(np.mean(self.Qra).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość Qrv: " + str(np.mean(self.Qrv).round(decimals=2)) + " [ml/s]\n"
            self.string_to_print += "Średnia wartość pra: " + str(np.mean(self.pra).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość prv: " + str(np.mean(self.prv).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość pap: " + str(np.mean(self.pap).round(decimals=2)) + " [mmHg]\n"
            self.string_to_print += "Średnia wartość Vra: " + str(np.mean(self.Vra).round(decimals=2)) + " [ml]\n"
            self.string_to_print += "Średnia wartość Vrv: " + str(np.mean(self.Vrv).round(decimals=2)) + " [ml]\n"

        self.gui.textEdit.setText(self.string_to_print)


def parameters_values():
    return 10, 30, 10, 30, 2.49, 0.049, 0.075, 0.523, 0.0243, 0.06, 0.000089, 0.0000594, 0.000416, 0.00005, 0.000206,\
           0.00005, 205, 370, 401, 596, 1938, 0.0334, 0.0824, 0.178, 0.667, 0.0223, 0.0267, 0.777, 1.64, 1.81, 13.24,\
           73.88, 0.00005, 0.00005, 50, 30, 53, 75, 75, 0.0251, 0.0227, 0.0530, 0.0379, 0.0252, 0.0126, 2.222, 1.481,\
           1.778, 6.666, 5, 0.00005, 0.00005


def starting_values():
    return [0.0], [0.0], [0.0], [0.0], [95.0], [109.0], [78.0], [99.0], [0.0], [0.0], [276.0], [506.0], [524.0],\
           [693.0], [2328.0], [0.0], [0.0], [91.4], [55.0], [74.0], [105.4], [105.0]


def fi_fun(t):
    t_fi = np.round(t - ((t // th) * th), decimals=5)
    if t_fi < tce:
        return (a * np.sin((np.pi * t_fi) / tce)) - (b * np.sin((2 * np.pi * t_fi) / tce))
    else:
        return 0


def elastance_fun(t, emin, emax):
    return emin * (1 - fi_fun(t)) + emax * fi_fun(t)


def pressure_fun1(E, V1, V2):
    return E * (V1 - V2)


def pressure_fun2(R, Q, p):
    return R * Q + p


def pressure_fun3(V1, V2, C):
    return (V1 - V2) / C


def blood_flow_fun(p1, p2, L, R, Q):
    return (p1 - p2) / L - (R * Q) / L


def volume_fun(Q1, Q2):
    return Q1 - Q2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    heart_simulation = HeartSimulation()
    heart_simulation.show()
    sys.exit(app.exec_())