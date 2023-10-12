################################################################################
# Imports
################################################################################

import socket
import selectors
import sys
import threading

################################################################################
# Constants, definitions and global variables
################################################################################

_HOST = '127.0.0.1'
_PORT = 57002
_MAX_MSG_SIZE = 4096

################################################################################
# Functions and procedures
################################################################################

_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else _PORT

################################################################################
# Classes
################################################################################

def dividir_lista(lista, tam):
    n = tam
    partes = []
    tam_lista = len(lista)
    
    for i in range(n):
        #print('valor de i > {}'.format(i))
        start = int((i * tam_lista) / n)
        end = int((i + 1) * tam_lista / n)
        #print(start)
        #print(end)
        partes.append(lista[start:end])
        #print(partes)
    #print(partes)
    return partes

def q_sort(numbers):
    legth = len(numbers) # CRIANDO UMA VARIAVEL QUE VAI GUARDAR O TAMANHO DO VETOR
    #CRIANDO UMA CONDIÇÃO PARA SAIR DA FUNÇÃO (QUANDO O TAMANHO CHEGAR A 0, ELE TERMINA)
    if legth <= 1:
        #q_sort.retorno += numbers
        return numbers
    # DECLARANDO UMA VARIAVEL DE TROCA (pop pega o ultimo valor do vetor)
    trade = numbers[-1]
    #print([trade])
    #print(trade)
    # CRIANDO 2 VETORES
    high, low, equal = [], [], []
    
    # LAÇO FOR DENTRO DO VETOR DE NUMEROS 
    for number in numbers:
        if number > trade:
            high.append(number)
        elif number < trade:
            low.append(number)
        else:
            equal.append(number)
    r = q_sort(low) + equal + q_sort(high)
    q_sort.retorno = r
    return r

    
################################################################################
# Main
################################################################################
if __name__ == "__main__":
    # Var Padrão
    sel = None     # Selector
    soc = None    # Socket para conexão
    key = None     # Auxiliar para trabalhar com os eventos
    mask = None    # Auxiliar para trabalhar com os eventos
    events = None  # Eventos recebidos do selector
    cmd000 = 'cmd000'
    
    a = None
    q_sort.retorno = []
    n_thread = 2
    
    # Inicializando nosso 'DefaultSelector'
    sel = selectors.DefaultSelector()
    
    # Criando o socket
    # AF_INET : formato (host, port)
    # SOCK_STREAM : TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configurando como não bloqueante
    soc.setblocking(False)
    
    # Conectando especial _ex (para ser nao bloqueante)
    soc.connect_ex((_HOST, _PORT))
    
    # Regsitrando nosso socket com o selector
    sel.register(soc, selectors.EVENT_READ)
    
    # Registrando o 'stdin' (usuário digitando) com o selector
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)
    
    soc.sendall(cmd000.encode())
    print('Enviada solicitação de cadastro ao Servidor...')
    
    ########################################
    # Loop principal
    ########################################
    while True:
        events = sel.select()
        
        for key, mask in events:
            # O usuário digitou algo
            if key.fileobj == sys.stdin.fileno():
                # Lendo a mensagem da entrada padrão
                data = sys.stdin.readline()
                
                
                
                # Sair
                if (data[:5]).lower() == '/exit':
                    print('Conexão Fechada !')
                    exit()   
                    
                    
                    
                # Tratando para não crashar o server
                else:
                    print('Error: Verifique se o comando está correto!')
                    
                    
                    
            # Recebendo respostas do Servidor
            else:
                # Recebendo os dados do socket
                data = key.fileobj.recv(_MAX_MSG_SIZE)
                data = data.decode()
                print(data)
                
                # Aqui começa o IF para tratar o vetor que recebemos do Servidor
                if data[:3] == 'qrt':
                    data = data[4:len(data) - 1]
                    data = data.split(',')
                    map_list = map(int, data)
                    lista = list(map_list)
                    print('Lista sem Ordenar > {}'.format(lista))
                    
                    lista_div = dividir_lista(lista, n_thread)
                    
                    th = []
                    h = []
                    
                    for i in range(n_thread):
                        th  = threading.Thread(
                            target=q_sort, args=[lista_div[i]])
                        th.start()
                        th.join()
                        h.append(q_sort.retorno)
                        
                    print(h)
                    
