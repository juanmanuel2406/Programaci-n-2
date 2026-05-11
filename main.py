from Logger import Loger
from activity import OtraActividad

my_log = Loger()
my_log.log("Iniciando la Aplicacion...")
my_log.log("A PUNTO DE REALIZXAR OTRA ACTIVIDAD...")
OtraActividad()
my_log.show_log()