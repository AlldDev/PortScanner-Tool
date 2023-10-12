# IMPORTs ###########################################################
import socket
import selectors
import threading
import sys
import concurrent.futures

# VAR GLOBALs #######################################################
_PORT_DEFAULT = [80, 8080, 442, 443, 22, 9991]
_PORT_ALL = range(1, 65536)
_N_THREADS = 2

# FUNCTIONs #########################################################
def p_scan(_HOST, _PORT):
    print('Iniciando')
    print('Host {} Port {}'.format(_HOST, _PORT))

    for i in range(len(_PORT)):
        if len(_PORT) <= 0:
            return

        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.settimeout(1)
            conn = soc.connect((_HOST, _PORT[i]))
            print('Porta Aberta > {}'.format(_PORT[i]))
            soc.close()
        except:
            print('Porta Fechada > {}'.format(_PORT[i]))
            # print('Porta Fechada > {}'.format(_PORT[i]))
        
    return

def divider(lista):
    parts = []
    tam_lista = len(lista)
    
    for i in range(_N_THREADS):
        start = int((i * tam_lista) / _N_THREADS)
        end = int((i + 1) * tam_lista / _N_THREADS)
        
        parts.append(lista[start:end])
        
    return parts
    
# MAIN ##############################################################
if __name__ == "__main__":
    # Variaveis



    # Seletor
    sel = selectors.DefaultSelector() # Iniciando Default
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)



    print('Digite /scan <host> <port>\n ou\nDigite /scan <host> default_port (para usar as portas default já definidass)')
    # Loop Principal ################################################
    while True:
        events = sel.select()
        
        for key, mask in events:
            # Verificando se o usuario digitou algo
            if key.fileobj == sys.stdin.fileno():
                data = sys.stdin.readline()

                if data[:5] == '/scan':
                    host, port = data[6:].split(' ', 2)
                    print('Host Inicial START{}END\nPorta Inicial START{}END'.format(host, port))
                    
                    if port[:len(port) - 1] == 'default_port':
                        port = _PORT_DEFAULT
                        
                    if port[:len(port) - 1] == 'all_port':
                        port = _PORT_ALL
                        port = list(port)
                        
                    ports = divider(port)
                    print('Portas Divididas pelas threads > {}'.format(ports))

                    for i in range(_N_THREADS):
                        print('Thread {} Iniciada...'.format(i))
                        th = threading.Thread(
                              target=p_scan, args=(host, ports[i]))
                        th.start()
                        th.join()
                        
                    #print('Host {} Port {}'.format(host, port))
                
            # Se receber algo de algum servidor
            else:
                data = key.fileobj.recv(1024)
