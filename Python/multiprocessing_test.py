from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
import os
import datetime

pid = os.getpid()

def first_formula_mp(conn: Connection, x: int) -> None:
    t_start = datetime.datetime.now()
    for _ in range(int(10e3)):
        f = x**2 - x**2 + 4*x - 5*x + x + x
    t_end = datetime.datetime.now()
    conn.send(t_end - t_start)
    conn.close()
    
def second_formula_mp(conn: Connection, x: int) -> None:
    t_start = datetime.datetime.now()
    for _ in range(int(10e4)):
        f = x + x
    t_end = datetime.datetime.now()
    conn.send(t_end - t_start)
    conn.close()
    
def third_formula_mp(conn: Connection, 
                     parent_conn1: Connection,
                     parent_conn2: Connection) -> None:
    data = {'f1':None, 'f2':None, 'f3':None}
    while True:
        try:
            data['f1'] = parent_conn1.recv()
        except:
            continue
        try:
            data['f2'] = parent_conn2.recv()
        except:
            continue
            
        if data['f1'] is not None and  data['f2'] is not None:
            data['f3'] = data['f1'] + data['f2']
            conn.send(data)
            conn.close()
            break
            
if __name__ == '__main__':
    parent_conn1, f1_conn = Pipe()
    parent_conn2, f2_conn = Pipe()
    parent_conn3, f3_conn = Pipe()
    
    f1 = Process(target=first_formula_mp, args=(f1_conn, 3))
    f2 = Process(target=second_formula_mp, args=(f2_conn, 4))    
    f3 = Process(target=third_formula_mp, args=(f3_conn, parent_conn1, parent_conn2))
    
    f1.start()
    f2.start()
    f3.start()
    f1.join()
    f2.join()
    f3.join()
    final_data = parent_conn3.recv()
   
    print(final_data)