import Menu as M
import Funzioni as F
import  DB as DB

def menu () :
    M.stampaMenu()

    scelta = input()
    while (scelta!='1' and scelta!='2' and scelta!='3' and scelta!='4' and scelta!='5' and scelta!='6') :
        M.stampaMenu()
        scelta = input()

    if (scelta=='1') :
        M.scelta1()
    if (scelta=='2') :
         M.scelta2()
    if (scelta=='3') :
         M.scelta3()
    if (scelta=='4') :
        M.scelta4()
    if (scelta=='5') :
        M.scelta5()
    if (scelta=='6') :
        M.scelta6()

if __name__ == '__main__':
    menu()
    DB.CreateDB()
