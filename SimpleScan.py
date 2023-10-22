# IMPORTs ###########################################################
import socket
import selectors
import threading
import sys
import os
import subprocess
import time
import pandas as pd

# from typing import List, Any

# VAR GLOBALs #######################################################
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
_DF = pd.read_csv('service-names-port-numbers.csv', sep=',', index_col='Port Number')


# FUNCTIONs #########################################################
def menuExibir():
    os.system('cls||clear')
    print(
        '  ████████ ██                      ██            ████████                           \n'
        ' ██░░░░░░ ░░              ██████  ░██           ██░░░░░░                            \n'
        '░██        ██ ██████████ ░██░░░██ ░██  █████   ░██         █████   ██████   ███████ \n'
        '░█████████░██░░██░░██░░██░██  ░██ ░██ ██░░░██  ░█████████ ██░░░██ ░░░░░░██ ░░██░░░██\n'
        '░░░░░░░░██░██ ░██ ░██ ░██░██████  ░██░███████  ░░░░░░░░██░██  ░░   ███████  ░██  ░██\n'
        '       ░██░██ ░██ ░██ ░██░██░░░   ░██░██░░░░          ░██░██   ██ ██░░░░██  ░██  ░██\n'
        ' ████████ ░██ ███ ░██ ░██░██      ███░░██████   ████████ ░░█████ ░░████████ ███  ░██\n'
        '░░░░░░░░  ░░ ░░░  ░░  ░░ ░░      ░░░  ░░░░░░   ░░░░░░░░   ░░░░░   ░░░░░░░░ ░░░   ░░ \n'
        '             -=- Uma simples ferramenta de scan -=- Leia o README.md -=-            \n'
        '                       -=- Precisa de ajuda? digite /help -=-                       \n'
    )


def menuHelp():
    os.system('cls||clear')
    menuExibir()
    print(
        '-=-MODO DE UTILIZAR -=-\n'
        '/scan <alvo> -p <porta> -m <modo>\n'
        '-------------------------------------------------------------\n'
        '<alvo> - IP ou Domínio.\n'
        '-------------------------------------------------------------\n'
        '<porta> -> Portas ou Protocolo\n'
        'Portas Especificas separar por Virgula (ex: 80,443,9050).\n'
        'default - Scaneia as 30 principais portas.\n'
        'all - Scaneia as 65536 portas, (Pode demorar um pouco).\n'
        '--------------------------------------------------------------\n'
        '<modo> -> Seleciona o timeout (Muito util)\n'
        'fast - (0.2s de timeout) - Recomendado para REDES LOCAIS.\n'
        'normal - (1s de timeout) - Recomendação PADRÃO.\n'
        'slow - (3s de timeout) - Recomendado para PAGINAS WEB com respostas lenta\n\n'
        '-=- EXEMPLO -=-\n'
        '/scan seusite.com.br -p default -m normal\n'
        '      ou 192.168.0.X\n'
    )


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
                    # print('Tentando UDP')
                    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    soc.settimeout(_TIMEOUT)
                    # print('Scaneando porta [{}]'.format(_PORT[i]))
                    conn = soc.connect((_HOST, _PORT[i]))
                    data = conn.recv(1024)
                    # service = socket.getservbyport(_PORT[i])
                    _PORTS_OPEN.append(_PORT[i])
                    soc.close()
                except:
                    pass
    except:
        print('Error ao realizar scan!!!')


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
        print('Nenhuma porta aberta foi identificada! (Alguns endereços precisam de um timeout maior).')
    else:
        print('Host: {}\n'.format(host))
        print('[STATUS] [PORTA]   [SERVIÇO EXECUTANDO]\n')

        for i in range(tam):
            try:
                #STR_PORT = str(_PORTS_OPEN[i])

                desc = _DF.loc[str(_PORTS_OPEN[i]), ['Description']].iloc[1].iloc[0]

                print('[Aberta] [{}] - {}'.format(_PORTS_OPEN[i], desc))


            except:
                try:
                    #print('Tentando descobrir serviço...')
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    soc.settimeout(3)
                    conn = soc.connect((host, _PORTS_OPEN[i]))
                    service = (socket.getservbyport(_PORTS_OPEN[i]))
                    print('[Aberta] [{}] - {}'.format(service))
                    soc.close()
                except:
                    print('[Aberta] [{}] - Não identificada'.format(_PORTS_OPEN[i]))
        print('\nScan concluido em {:.2f} segundos!'.format(t_total))
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
def ping_host(host):
    if sys.platform.startswith('win'):
        cmd = ['ping', '-n', '1', host]
    else:
        cmd = ['ping', '-c', '1', host]

    try:
        output = subprocess.check_output(cmd)
        print('Host {} ativo.'.format(host))
        return True
    except:
        print('Host {} não acessivel.'.format(host))
        return False


# MAIN ##############################################################
if __name__ == "__main__":
    # Variaveis
    th = []

    menuExibir()
    # Loop Principal ################################################
    while True:
        print('Digite:')
        data = sys.stdin.readline()

        # Se precisar de ajuda.
        if data[:5] == '/help':
            menuHelp()

        # Se quiser fechar o sistema de maneira correta
        if data[:5] == '/exit':
            menuExibir()
            print('Espero vê-lo em breve !!! Até mais ;D')
            sys.exit()

        # Para começar o Scan
        if data[:5] == '/scan':
            menuExibir()
            host, p, port, m, modo = data[6:].split()  # Divido a Entrada para tratar cada parte
            # print('{}\n{}\n{}\n{}\n{}'.format(host, p, port, m, modo))
            # ativo = ping_host(host)  # Verifico se o Host está ativo antes de começar

            # Se estiver ativo, ele começa a Scanear
            # (Desativado, Muitos hosts não responde Ping... deixei apenas if True para se um dia quiser voltar...)
            if True:
                print('Iniciando Serviços...')
                try:
                    # host, port = data[6:].split(' ', 2)
                    print('Scaneando Host {}.\nPor favor, Aguarde...'.format(host))
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
                        print(port)
                    else:
                        print('Erro na declaração das portas!\nDuvidas digite /help.')
                        continue

                    # Verificando o modo selecionado
                    if m == '-m':
                        if modo == 'normal':
                            timeout = 1
                        elif modo == 'fast':
                            timeout = 0.2
                        elif modo == 'slow':
                            timeout = 3
                        else:
                            print('Modo "{}" não existe!\nDuvidas digite /help.'.format(modo))

                        # print('len de Ports {}'.format(len(port)))

                        # Aqui eu verifico o tanto de portas para não criar threads atoa.
                        if len(port) <= os.cpu_count() * 2:
                            _N_THREADS = len(port)

                        elif len(port) > os.cpu_count() * 2:
                            _N_THREADS = os.cpu_count() * 2

                    else:
                        print('Erro na declaração dos modos!\nDuvidas digite /help.')
                        continue

                except:
                    print('Erro na entrada!\nDuvidas digite /help.')
                    continue

                ports = divider(port)  # Dividindo as portas pelo número de threads

                t_inicio = time.time()
                for i in range(_N_THREADS):
                    # print('Thread {} Iniciada...'.format(i))
                    th.append(threading.Thread(
                        target=p_scan, args=(host_ip, ports[i], timeout)))
                    th[i].start()

                for i in range(len(th)):
                    # print('Aguardando Thread {} Terminar'.format(i))
                    th[i].join()
                t_fim = time.time()
                t_total = t_fim - t_inicio

                th = []  # limpo o vetor de threads para poder reutiliza-lo

                # time.sleep(5)
                exibir(host_name_ip, t_total)
                _PORTS_OPEN = []  # Limpando vetor para reutilizar na proxima interação
                _N_THREADS = os.cpu_count()  # Resetando o vetor de Threads

            else:
                print('Falha geral! Contate o suporte!\n"la garantía soy yo."')
