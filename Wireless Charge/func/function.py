
import math

def getDCIn(Dac):
  DCIn = 21*3.3*Dac/4096

  return DCIn


def getVcoil(Dac):
  Vcoil = 101*3.3*Dac/4096

  return Vcoil

def getIsens(Dac):
  Isens = abs(0.000023042*Dac-8.5714)/20

  return Isens

def getTsens(Dac):
  Vt = 3.3*Dac/4096
  Rt = 10000*Vt/(3.3-Vt)
  T = 1/(math.log(Rt/10000)/4100+1/298.15)-273.15

  return T
  
