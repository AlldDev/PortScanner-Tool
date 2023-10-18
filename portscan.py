# IMPORTs ###########################################################
import socket
import selectors
import threading
import sys
import os
import subprocess
import time

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


# FUNCTIONs #########################################################
def menuExibir():
    os.system('cls||clear')
    print(
        '   ▄████████  ▄█    ▄▄▄▄███▄▄▄▄      ▄███████▄  ▄█          ▄████████         ▄████████  ▄████████    ▄████████ ███▄▄▄▄   \n'
        '  ███    ███ ███  ▄██▀▀▀███▀▀▀██▄   ███    ███ ███         ███    ███        ███    ███ ███    ███   ███    ███ ███▀▀▀██▄ \n'
        '  ███    █▀  ███▌ ███   ███   ███   ███    ███ ███         ███    █▀         ███    █▀  ███    █▀    ███    ███ ███   ███ \n'
        '  ███        ███▌ ███   ███   ███   ███    ███ ███        ▄███▄▄▄            ███        ███          ███    ███ ███   ███ \n'
        '▀███████████ ███▌ ███   ███   ███ ▀█████████▀  ███       ▀▀███▀▀▀          ▀███████████ ███        ▀███████████ ███   ███ \n'
        '         ███ ███  ███   ███   ███   ███        ███         ███    █▄                ███ ███    █▄    ███    ███ ███   ███ \n'
        '   ▄█    ███ ███  ███   ███   ███   ███        ███▌    ▄   ███    ███         ▄█    ███ ███    ███   ███    ███ ███   ███ \n'
        ' ▄████████▀  █▀    ▀█   ███   █▀   ▄████▀      █████▄▄██   ██████████       ▄████████▀  ████████▀    ███    █▀   ▀█   █▀  \n'
        '                                               ▀                                                                          \n'
        '    -=- Uma simples ferramenta de scan -=- Leia o README.md -=- Uma simples ferramenta de scan -=- Leia o README.md -=-   \n'
        '                                        -=- Precisa de ajuda? digite /help -=-                                            \n'
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
        'fast - (1s de timeout)\n'
        'normal - (1.5s de timeout)\n'
        'slow - (4s de timeout)\n\n'
        '-=- EXEMPLO -=-\n'
        '/scan seusite.com.br -p default -m fast\n'
        '      ou 192.168.0.X\n'
    )


def p_scan(_HOST, _PORT, _TIMEOUT):
    try:
        for i in range(len(_PORT)):
            if len(_PORT) <= 0:
                return

            try:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.settimeout(_TIMEOUT)
                # print('Scaneando porta [{}]'.format(_PORT[i]))
                conn = soc.connect((_HOST, _PORT[i]))
                # service = socket.getservbyport(_PORT[i])
                _PORTS_OPEN.append(_PORT[i])
                soc.close()
            except:
                pass
    except:
        print('Error ao realizar scan!!!')


def divider(lista):
    parts = []
    tam_lista = len(lista)

    for i in range(_N_THREADS):
        start = int((i * tam_lista) / _N_THREADS)
        end = int((i + 1) * tam_lista / _N_THREADS)

        parts.append(lista[start:end])
    return parts


def exibir(host, _PORTS_OPEN, t_total):
    menuExibir()

    tam = len(_PORTS_OPEN)
    _PORTS_OPEN.sort()

    if tam <= 0:
        print('Nenhuma porta aberta foi identificada! (Alguns endereços precisam de um timeout maior).')
    else:
        print('Host: {}\n'.format(host))
        print('[STATUS] [PORTA]   [SERVIÇO EXECUTANDO]\n')
        for i in range(tam):
            if _PORTS_OPEN[i] in protocols:
                print('[Aberta] [{}] - {}'.format(_PORTS_OPEN[i], protocols[_PORTS_OPEN[i]]))
            else:
                try:
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    soc.settimeout(3)
                    conn = soc.connect((host, _PORTS_OPEN[i]))
                    service = socket.getservbyport(_PORTS_OPEN[i])
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
    protocols = {
        20: "FTP (File Transfer Protocol - Data)",
        21: "FTP (File Transfer Protocol - Control)",
        22: "SSH (Secure Shell)",
        23: "Telnet (acesso remoto não seguro)",
        25: "SMTP (Simple Mail Transfer Protocol)",
        53: "DNS (Domain Name System)",
        67: "DHCP (Dynamic Host Configuration Protocol)",
        68: "DHCP (Dynamic Host Configuration Protocol)",
        69: "TFTP (Trivial File Transfer Protocol)",
        80: "HTTP (Hypertext Transfer Protocol)",
        88: "Kerberos",
        110: "POP3 (Post Office Protocol, versão 3)",
        111: "RPC (Remote Procedure Call)",
        119: "NNTP (Network News Transfer Protocol)",
        123: "NTP (Network Time Protocol)",
        135: "MS RPC (Microsoft Remote Procedure Call)",
        137: "NetBIOS",
        138: "NetBIOS",
        139: "NetBIOS",
        143: "IMAP (Internet Message Access Protocol)",
        161: "SNMP (Simple Network Management Protocol)",
        162: "SNMP (Simple Network Management Protocol)",
        389: "LDAP (Lightweight Directory Access Protocol)",
        443: "HTTPS (HTTP Secure)",
        445: "Microsoft-DS (Microsoft Directory Services)",
        465: "SMTP com SSL/TLS",
        514: "Syslog (Protocolo de registro de sistema)",
        515: "LPD (Line Printer Daemon)",
        587: "Submission (envio seguro de e-mails)",
        636: "LDAPS (LDAP com segurança)",
        993: "IMAP com SSL/TLS",
        995: "POP3 com SSL/TLS",
        1080: "SOCKS (Proxy de rede)",
        1099: "RMI (Java Remote Method Invocation)",
        1433: "MSSQL (Microsoft SQL Server)",
        6660: "Internet Relay Chat (IRC)",
        6661: "Internet Relay Chat (IRC)",
        6665: "Internet Relay Chat (IRC)",
        6666: "Internet Relay Chat (IRC)",
        6667: "Internet Relay Chat (IRC)",
        6668: "Internet Relay Chat (IRC)",
        6669: "Internet Relay Chat (IRC)",
        6697: "Internet Relay Chat (IRC)",
        8000: "HTTP alternativo",
        8008: "HTTP alternativo",
        8443: "HTTPS alternativo",
        1521: "Oracle Database",
        3306: "MySQL",
        5432: "PostgreSQL",
        5900: "VNC (Virtual Network Computing)",
        9100: "JetDirect (HP JetDirect)",
        49152: "Backdoor Diamond (proposta pelo IANA)",
        1: "TCPMUX - Serviço de porta TCP",
        5: "RJE - Entrada remota de trabalho",
        7: "ECHO - Protocolo de eco",
        11: "SYSTAT - Listagem de status de sistema",
        17: "QOTD - Citação do dia",
        43: "WHOIS - Serviço de informações de nome de domínio",
        77: "RJE - Entrada remota de trabalho",
        101: "NIC Host Name",
        102: "ISO-TSAP - Protocolo de acesso a serviços de transporte",
        103: "gopher - Protocolo Gopher",
        109: "POP2 - Post Office Protocol, versão 2",
        115: "SFTP - Protocolo simples de transferência de arquivos",
        118: "SQL Serviços alternativos",
        427: "SLP - Protocolo de localização de serviços",
        513: "rlogin - Login remoto",
        540: "UUCP - Protocolo UUCP",
        554: "RTSP - Protocolo de streaming em tempo real",
        902: "VMware Server Console",
        989: "FTPS - FTP com SSL",
        992: "Telnet com SSL",
        1026: "IIS",
        1027: "IIS",
        1028: "IIS",
        1029: "IIS",
        1110: "NFS",
        1725: "Steam",
        1741: "CiscoWorks 2000",
        2179: "Microsoft Firewall Storage",
        179: "BGP (Border Gateway Protocol)",
        194: "IRC (Internet Relay Chat)",
        1025: "NFS ou IIS ou portas de RPC",
        1701: "L2TP (Layer 2 Tunneling Protocol)",
        2049: "NFS - Protocolo de sistema de arquivos em rede",
        3128: "Squid (HTTP Proxy)",
        3389: "RDP - Protocolo de área de trabalho remota",
        5631: "pcAnywhere",
        5632: "pcAnywhere",
        5901: "VNC (Virtual Network Computing)",
        6346: "Gnutella (File Sharing)",
        6347: "Gnutella (File Sharing)",
        6881: "BitTorrent",
        6882: "BitTorrent",
        6883: "BitTorrent",
        6884: "BitTorrent",
        6885: "BitTorrent",
        6886: "BitTorrent",
        6887: "BitTorrent",
        6888: "BitTorrent",
        6889: "BitTorrent",
        6969: "BitTorrent",
        7000: "Default para UPnP (Universal Plug and Play)",
        9000: "CSlistener (Java RMI)",
        9999: "HTTP alternativo",
        10000: "Webmin",
        10255: "Kubernetes API Server",
        11211: "Memcached",
        27017: "MongoDB",
        28015: "RethinkDB",
        50000: "Default para League of Legends (LoL)",
        50070: "Hadoop",
        50075: "Hadoop",
        50090: "Hadoop",
        60000: "Deep Discovery",
        6379: "Redis",
        8080: "HTTP alternativo",
        8081: "HTTP alternativo",
        8888: "HTTP alternativo",
        9418: "Git",
        9050: "Proxy TOR", }

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
                        port = port[3:len(port) - 1].split(',')
                        port_div = []
                        for i in range(len(port)):
                            port_div.append(int(port[i]))
                        port = port_div
                    else:
                        print('Erro na declaração das portas!\nDuvidas digite /help.')
                        continue

                    # Verificando o modo selecionado
                    if m == '-m':
                        if modo == 'normal':
                            timeout = 1.5
                        elif modo == 'fast':
                            timeout = 1
                        elif modo == 'slow':
                            timeout = 4
                        else:
                            print('Modo "{}" não existe!\nDuvidas digite /help.'.format(modo))
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

                exibir(host_name_ip, _PORTS_OPEN, t_total)
                _PORTS_OPEN = []  # Limpando vetor para reutilizar na proxima interação

            else:
                print('Tente novamente...')
