# coding=utf-8

import sqlite3

from datetime import datetime
import time

con = sqlite3.connect('test.db')

class MiError(Exception):
    def __init__(self, valor):
        self.valor = valor
    def __str__(self):
        return repr(self.valor)

def conexion_db():

    #coneccion = sqlite3.connect(':memory:')
    cursor = con.cursor()
    return cursor

def crea_tablas(cursor):

    cursor.execute('''CREATE TABLE EMPRESA
        (ID INT PRIMARY KEY     NOT NULL,
        NOMBRE          TEXT    NOT NULL,
        APELLIDO        TEXT    NOT NULL,
        SUELDO_BASE     REAL    NOT NULL,
        FECHA_INGRESO   TEXT     NOT NULL,
        AFAP            INT     NOT NULL,
        HIJOS           INT )''')
    print "Tabla creada con exito"
    con.close()

def inserta_datos(cursor):

    datos = [(),(),(),(),()]
    nombre = raw_input("Ingrese el nombre del trabajador ")
    apellido = raw_input("Ingrese el apellido del trabajador ")
    sueldo = int(input("Ingrese el sueldo base "))
    fecha = raw_input("Ingrese la fecha de ingreso: formato dd/mm/año ")
    afap = int(input("Ingrese 1 si el AFAP cobra 12% o 2 si cobra 11.4% "))
    hijos = int(input("Ingrese la cantidad de hijos del trabajador "))
    datos.append([(nombre),(apellido),(sueldo),(fecha),(afap),(hijos)])
    cursor.execute("INSERT INTO EMPRESA (NOMBRE, APELLIDO, SUELDO_BASE, FECHA_INGRESO, AFAP, HIJOS) \
        VALUES('%s','%s','%d','%s','%d','%d')" % (nombre,apellido,sueldo,fecha,afap,hijos))
    print datos
    global con
    con.commit()

def consultas(cursor):

    empleado_usuario = raw_input("Ingrese el nombre de un empleado para hacer consultas de sueldo ")
    string_sql="SELECT ID, NOMBRE, APELLIDO, SUELDO_BASE, FECHA_INGRESO, AFAP, HIJOS from EMPRESA where NOMBRE like '{}'".format(empleado_usuario)
    cursor.execute(string_sql)
    try:
        for i in cursor:

            if i[1] == empleado_usuario:
                formato = "%d/%m/%y"
                fecha_actual = str(time.strftime("%d/%m/%y"))
                fecha = i[4]
                fecha = datetime.strptime(fecha, formato)
                fecha_actual = datetime.strptime(fecha_actual, formato)
                if fecha_actual > fecha:
                    dif = fecha_actual - fecha
                    diff_seconds = (dif).total_seconds()
                    dif = int(diff_seconds)/60/60/24/30
                if i[6] != 0 or dif != 1:
                    base_imponible = i[3] + ((i[3]*0.01)*dif) + ((i[3]*0.05)*i[6])
                fonasa = base_imponible * 0.07
                print "El monto a pagar a fonasa de este trabajador es " + str(fonasa)
                if i[5] == 1:
                    monto_afap = base_imponible * 0.12
                elif i[5] == 2:
                    monto_afap = base_imponible * 0.12
                print "El monto a pagar a AFAP de este trabajador es " + str(monto_afap)
                base_imponible = base_imponible - fonasa - monto_afap
                print "El sueldo a pagar, con deducciones y prestaciones " + str(base_imponible)
            else:
                print "El nombre no existe en la base de datos, intente nuevamente"
    except:
        print "El nombre no existe en la base de datos, intente nuevamente"



def promedio(cursor):

    string_sql="SELECT ID, SUELDO_BASE from EMPRESA"
    cursor.execute(string_sql)
    sueldos = []
    promedio, suma_sueldos = 0,0
    for i in cursor:
        sueldos = i[1]
        suma_sueldos = suma_sueldos + sueldos
        promedio = suma_sueldos / i[0]

    print "El promedio de sueldos de los empleados es " + str(promedio)

def main():
    menu = True
    while True:

        print("\n")
        menu_opciones()
        choice = int(raw_input("\nInserte opcion de menu: "))
        print("\n")
        if choice==1:
            inserta_datos(conexion_db())
        elif choice==2:
            consultas(conexion_db())
        elif choice==3:
            promedio(conexion_db())
        elif choice==0:
            print "Gracias por usar el software"
            menu = False
        else:
            print "Puso una opcion no valida"
    con.close()


def menu_opciones():
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. Cargar nuevo empleado"
    print "2. Realizar consulta de salario de un empleado"
    print "3. Calcular promedio sueldo"
    print "0. Salir"
    print 67 * "-"

conexion_db()
main()

