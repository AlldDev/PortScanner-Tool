###########################################################
# IMPORTs
###########################################################
import socket
import selectors
import threading
import sys
import os
#import subprocess
import time
import pandas as pd
import numpy as np

###########################################################
# CORES
###########################################################
cores = {
    "limpar": "\033[m",
    "branco": "\033[1;30m",
    "vermelho": "\033[1;31m",
    "verde": "\033[1;32m",
    "amarelo": "\033[1;33m",
    "azul": "\033[1;34m",
    "magenta": "\033[1;35m",
    "ciano": "\033[1;36m",
    "cinza": "\033[1;37m",
}

###########################################################
# VAR GLOBALs
###########################################################
_PORT_DEFAULT = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 88, 110, 111, 119, 123, 135, 137, 138, 139, 143,
    161, 162, 179, 194, 389, 443, 445, 465, 514, 515, 587, 636, 993, 995, 1080, 1099, 1433,
    3306, 6666, 8443, 1521, 27017, 3389, 5432, 5900, 6660, 6661, 6665, 6667, 6668, 6669,
    6697, 7000, 8000, 8008, 8080, 8081, 9000, 9100, 9999, 10000, 50000, 49152,
    119, 375, 425, 1214, 412, 1412, 2412, 4661, 4662, 4665, 5500, 6346, 6881,
    6882, 6883, 6884, 6885, 6886, 6887, 6888, 6889]

_PORT_ALL = range(1, 65536)
_PORTS_INPUT = []
_PORTS_OPEN = []
_N_THREADS = (os.cpu_count()) * 2
_DF = pd.read_csv('services-port.csv', sep=',', index_col='Port Number')
#print(_DF)
#_DF = _DF['Port Number'].replace('', np.nan, inplace=True)
#print(_DF)
#time.sleep(50)
#_DF.dropna(subset=['Port Number'], inplace=True)
#print(_DF)
#time.sleep(50)
#_DF.sort_values(by=['Port Number'])

###########################################################
# FUNCTIONs
###########################################################
def menuExibir():
    os.system('cls||clear')
    print(f'''{cores['ciano']}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⡀⠠⣼⠄⠵⠒⠂⠉⢇⡋⠉⠓⠀⠀⠄⠹⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢆⠄⠄⠢⠅⡄⣔⢁⠁⠀⠡⠍⢁⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⡁⠀⠀⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡐⠀⠀⡘⠀⠀⠀⡄⠀⠉⠁⠘⠫⢀⡠⠄⣀⡤⠤⢶⡳⢿⠯⠭⠯⢭⠾⣥⣐⡃⠂⢄⠀⠑⢴⡠⡈⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢇⠀⠀⠡⠣⠄⡒⠖⠉⠁⡄⢀⡠⣆⢿⠵⠏⠙⠑⡁⡰⡁⡀⣃⢇⢄⣆⠄⠣⡋⠋⠝⡿⢵⠽⡀⠉⠕⢊⡁⠰⠀⠀⠰⠀⠀⠀⠀⠀⠀
⢅⡡⢄⣨⡩⠖⠊⠀⣁⢕⣿⠏⡕⣦⢯⢱⣯⡿⣿⠽⡟⡖⣟⠅⠊⠄⠆⠉⠹⢳⡹⡇⠀⠀⠁⠊⢿⢕⠌⡉⠁⠑⣔⡠⡇⠀⠀⠀
⠀⠬⡩⠚⢁⠲⣮⡪⢋⠊⠀⠐⢼⠊⠒⠽⢫⣿⣷⣯⣽⣧⣘⠘⢌⠜⠈⠕⠄⠁⠉⣋⢣⠀⠀⠀⠀⠀⠉⢓⠷⣄⠀⠈⠀⠉⢱⠀⠀
⠀⠀⠀⠉⡡⢿⠏⠁⠂⠇⠁⣄⣯⡬⣛⣿⣿⡿⣾⢻⣿⣿⣿⡷⠁⡯⠮⣃⢀⠠⠃⠀⠂⡓⡀⠀⠀⠀⠀⠀⠀⠡⠉⣧⡀⠀⠀⠀⠀⠀┏┓       ┏┓             ┏┳┓    ┓
⠀⠀⡜⢁⠺⠁⠀⡠⢨⠀⠤⡡⢾⣏⢷⣿⣟⣿⡯⣯⡾⡿⠯⢿⠬⡏⠠⠉⠀⠉⠃⠉⠸⡏⡀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡷⡻⢆⠀⠀⠀┃┃┏┓┏┓╋  ┗┓┏┏┓┏┓┏┓┏┓┏┓   ┃ ┏┓┏┓┃
⠀⠀⣿⠁⠠⡀⠀⠀⠘⡍⠉⠡⠵⡿⠗⢔⠿⡿⡾⢟⠷⠏⡿⢿⡯⠈⡗⠬⠀⣄⠐⠀⡜⠁⡁⠀⠀⠀⠀⢀⡠⠴⣫⠟⠙⠈⠀⠀⠀ ┣┛┗┛┛ ┗  ┗┛┗┗┻┛┗┛┗┗ ┛    ┻ ┗┛┗┛┗
⠀⠀⠈⠙⠧⠷⣭⣓⠦⢷⣎⠂⠠⡉⣔⡎⠍⡏⢇⡂⡖⠠⠧⡗⢰⡃⠀⢀⡀⡲⡯⢤⡲⠾⠋⠉⢁⠠⣤⠔⡉⠉⠑⢄⠀⠀⠀⠀⠀
⠀⠀⢠⡔⡯⡄⠀⠀⠉⡉⠓⠊⠿⠿⢾⢕⣮⣥⣶⡽⣧⣥⣵⠿⡭⠭⠶⠦⠝⠚⠂⠒⡒⠩⠁⠈⠀⡄⠀⠀⠁⠖⠀⠈⠂⠀⠀⠀⠀⠀           by github.com/AlldDev
⠀⠀⠃⠳⣠⡄⢀⡴⠟⠀⠀⠀⢠⠀⠀⠀⠀⠀⠏⠸⠀⠈⡇⠁⠁⠀⠁⠁⠈⠈⣠⠈⠀⠀⢙⣢⡀⠄⠀⠘⢤⠤⠠⠈⠃⠀⠀⠇⠀⠀
⠀⠀⢸⠏⠀⠀⠽⠉⠉⠉⠉⠨⡇⠀⡄⠀⠀⣨⡆⣀⣘⡀⡀⢣⠱⡗⠈⠁⢙⡍⡇⠉⠈⣽⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⠅⠀⠀⢲⠀⠀⠀⠀⠀⡓⡭⠂⠃⠤⠄⠦⠡⠀⠸⠀⠀⠀⠸⠂⠁⠀⠀⠀⠋⠀⠀⠀⠨⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀⠀⠁⠘⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                                                                                                                                                                                                                                                                                                                       
{cores['limpar']} ''')

def menuHelp():
    os.system('cls||clear')
    menuExibir()
    print(f'''{cores['vermelho']}* MODO DE UTILIZAR{cores['limpar']}
/scan {cores['ciano']}<alvo>{cores['limpar']} -p {cores['ciano']}<porta>{cores['limpar']} -m {cores['ciano']}<modo>{cores['limpar']}

{cores['ciano']}<alvo>{cores['limpar']}  - IP ou Domínio.

{cores['ciano']}<porta>{cores['limpar']} - Portas ou Protocolo
          Portas Especificas separar por Virgula (ex: 80,443,9050).
          {cores['amarelo']}default{cores['limpar']} - Scaneia as 30 principais portas.
          {cores['amarelo']}all{cores['limpar']} - Scaneia as 65536 portas, (Pode demorar um pouco).

{cores['ciano']}<modo>{cores['limpar']}  - Seleciona o timeout (Muito util)
          {cores['amarelo']}fast{cores['limpar']} - (0.2s de timeout) - Recomendado para REDES LOCAIS.
          {cores['amarelo']}normal{cores['limpar']} - (1s de timeout) - Recomendação PADRÃO.
          {cores['amarelo']}slow{cores['limpar']} - (3s de timeout) - Recomendado para PAGINAS WEB com respostas lenta
{cores['vermelho']}* EXEMPLO{cores['limpar']}
/scan {cores['ciano']}seusite.com.br{cores['limpar']} -p {cores['ciano']}default{cores['limpar']} -m {cores['ciano']}normal{cores['limpar']}''')

def p_scan(_HOST, _PORT, _TIMEOUT):
    global _PORTS_OPEN
    data = None
    try:
        for i in range(len(_PORT)):
            if len(_PORT) <= 0:
                return

            # Tentando conectar via TCP/IP
            try:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.settimeout(_TIMEOUT)
                # print('Scaneando porta [{}]'.format(_PORT[i]))
                conn = soc.connect((_HOST, _PORT[i]))
                # service = socket.getservbyport(_PORT[i])
                _PORTS_OPEN.append(_PORT[i])
                soc.close()
            except:
                # Tentando conectar via UDP
                try:
                    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    soc.settimeout(_TIMEOUT)
                    conn = soc.connect((_HOST, _PORT[i]))
                    data = conn.recv(1024)
                    # service = socket.getservbyport(_PORT[i])
                    _PORTS_OPEN.append(_PORT[i])
                    soc.close()
                except:
                    pass
    except:
        print(f'''{cores['vermelho']}Error ao realizar scan!!!{cores['limpar']}''')


def divider(lista):
    global _N_THREADS

    parts = []
    tam_lista = len(lista)

    for i in range(_N_THREADS):
        start = int((i * tam_lista) / _N_THREADS)
        end = int((i + 1) * tam_lista / _N_THREADS)

        parts.append(lista[start:end])
    return parts


def exibir(host, t_total):
    global _DF
    global _PORTS_OPEN
    tam = len(_PORTS_OPEN)
    _PORTS_OPEN.sort()
    menuExibir()

    if tam <= 0:
        print(f'''{cores['vermelho']}Nenhuma porta aberta foi identificada! (Alguns endereços precisam de um timeout maior).{cores['limpar']}''')
    else:
        print(f'''Target: {cores['ciano']}{host}{cores['limpar']}''')
        print("[STATUS] [PORTA]   [SERVIÇO EXECUTANDO]")


        for i in range(tam):
            try:
                #STR_PORT = str(_PORTS_OPEN[i])

                desc = _DF.loc[str(_PORTS_OPEN[i]), ['Description']].iloc[1].iloc[0]

                print(f'''[{cores['ciano']}Aberta{cores['limpar']}] [{cores['ciano']}{_PORTS_OPEN[i]}{cores['limpar']}] - {cores['ciano']}{desc}{cores['limpar']}''')

            except:
                try:
                    #print('Tentando descobrir serviço...')
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    soc.settimeout(3)
                    conn = soc.connect((host, _PORTS_OPEN[i]))
                    service = (socket.getservbyport(_PORTS_OPEN[i]))
                    print(f'[Aberta] [{host}] - {service}')
                    soc.close()
                except:
                    print(f'''[{cores['ciano']}Aberta{cores['limpar']}] [{cores['ciano']}{_PORTS_OPEN[i]}{cores['limpar']}] - {cores['ciano']}Não identificada{cores['limpar']}''')
        print('\n{}Scan concluido em {:.2f} segundos!{}'.format(cores['amarelo'], t_total, cores['limpar']))
        _PORTS_OPEN = []  # Zerando o vetor para uma proxima verificação


def get_ip(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except:
        return host


# Função não utilizada, pois alguns hosts não responde ao ping
# com isso, deixamos de scanear... então decidi não utilizar mais
# o ping antes, fazendo o Scan direto...
#def ping_host(host):
    #if sys.platform.startswith('win'):
        #cmd = ['ping', '-n', '1', host]
    #else:
        #cmd = ['ping', '-c', '1', host]

    #try:
        #output = subprocess.check_output(cmd)
        #print('Host {} ativo.'.format(host))
        #return True
    #except:
        #print('Host {} não acessivel.'.format(host))
        #return False

###########################################################
# MAIN
###########################################################
if __name__ == "__main__":
    # Variaveis
    th = []
    menuExibir()

    #####################
    # Loop Principal
    #####################
    while True:
        print(f'''{cores['ciano']}scan: {cores['limpar']}''', end='')
        data = sys.stdin.readline()

        # Se precisar de ajuda.
        if data[:5] == '/help':
            menuHelp()

        # Se quiser fechar o sistema de maneira correta
        if data[:5] == '/exit':
            menuExibir()
            print(f'''{cores['azul']}Espero vê-lo em breve !!! Até mais ;D{cores['limpar']}''')
            sys.exit()

        # Para começar o Scan
        if data[:5] == '/scan':
            menuExibir()
            host, p, port, m, modo = data[6:].split()  # Divido a Entrada para tratar cada parte

            # ativo = ping_host(host)  # Verifico se o Host está ativo antes de começar
            # Se estiver ativo, ele começa a Scanear
            # (Desativado, Muitos hosts não responde Ping... deixei apenas if True para se um dia quiser voltar...)
            if True:
                print(f'''{cores['vermelho']}Iniciando Serviços...{cores['limpar']}''')
                try:
                    # host, port = data[6:].split(' ', 2)
                    print(f'''{cores['vermelho']}Scaneando Host {host}.\nPor favor, Aguarde...{cores['limpar']}''')
                    host_ip = get_ip(host)  # Aqui ele pega o IP caso o usuário tenha passado um Dominio

                    # Apenas Verifico para quando exibir aparecer o IP, ou se for dominio
                    # aparecer o dominio juntamente com o IP (resolvido DNS)
                    if host == host_ip:
                        host_name_ip = host_ip
                    else:
                        host_name_ip = host + " - " + host_ip

                    # Verificação se o usuário digitou a porta ou selecionou uma
                    # das opções já existentes
                    if port == 'default':
                        port = _PORT_DEFAULT
                    elif port == 'all':
                        port = _PORT_ALL
                    elif p == '-p':
                        # port = port[3:len(port) - 1].split(',')
                        port = port.split(',')
                        port_div = []
                        for i in range(len(port)):
                            port_div.append(int(port[i]))
                        port = port_div
                        #print(port)
                    else:
                        print(f'''{cores['vermelho']}Erro na declaração das portas!\nDuvidas digite /help.''')
                        continue

                    # Verificando o modo selecionado
                    if m == '-m':
                        if modo == 'normal':
                            timeout = 0.5
                        elif modo == 'fast':
                            timeout = 0.2
                        elif modo == 'slow':
                            timeout = 2
                        else:
                            print(f'''{cores['vermelho']}Modo "{modo}" não existe!\nDuvidas digite /help.{cores['limpar']}''')

                        # print('len de Ports {}'.format(len(port)))

                        # Aqui eu verifico o tanto de portas para não criar threads atoa.
                        if len(port) <= os.cpu_count() * 2:
                            _N_THREADS = len(port)

                        elif len(port) > os.cpu_count() * 2:
                            _N_THREADS = os.cpu_count() * 2

                    else:
                        print(f'''{cores['vermelho']}Erro na declaração dos modos!\nDuvidas digite /help.{cores['limpar']}''')
                        continue

                except:
                    print(f'''{cores['vermelho']}Erro na entrada!\nDuvidas digite /help.{cores['limpar']}''')
                    continue

                ports = divider(port)  # Dividindo as portas pelo número de threads

                t_inicio = time.time()
                for i in range(_N_THREADS):
                    th.append(threading.Thread(
                        target=p_scan, args=(host_ip, ports[i], timeout)))
                    th[i].start()

                for i in range(len(th)):
                    th[i].join()
                t_fim = time.time()
                t_total = t_fim - t_inicio

                th = []  # limpo o vetor de threads para poder reutiliza-lo

                # time.sleep(5)
                exibir(host_name_ip, t_total)
                _PORTS_OPEN = []  # Limpando vetor para reutilizar na proxima interação
                _N_THREADS = os.cpu_count()  # Resetando o vetor de Threads

            else:
                print(f'''{cores['vermelho']}Falha geral! Contate o suporte!\n"la garantía soy yo."{cores['limpar']}''')
