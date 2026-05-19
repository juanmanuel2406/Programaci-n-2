from factorys import Mpfactory, Cardfactory, Paypalfactory
from payhelper import checkout

factory = Paypalfactory()

checkout(factory, 50000)