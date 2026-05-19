<<<<<<< HEAD
from factorys import Mpfactory, Cardfactory, Paypalfactory
from payhelper import checkout

factory = Paypalfactory()

checkout(factory, 50000)
=======
from Logger import Loger
from activity import OtraActividad

my_log = Loger()
my_log.log("Iniciando la Aplicacion...")
my_log.log("A PUNTO DE REALIZXAR OTRA ACTIVIDAD...")
OtraActividad()
my_log.show_log()
>>>>>>> 824990ac8c4e7ed10cb26f04227a04d220d2d763
