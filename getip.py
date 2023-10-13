import socket


def get_ip(host):
    try:
        ip = socket.gethostbyname(host)
        print('o host {} é o ip {}'.format(host, ip))
        return ip
    except:
        print('o ip enviado é {}'.format(host))
        return host

entry = input('Digite')

print(get_ip(entry))
