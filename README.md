# SimpleScan

![Screenshot ](assets/icon.ico)

## Sobre:

> Uma simples ferramenta para scan de redes !

## Detalhes:
> Ferramenta desenvolvida pensando no auxilio ao suporte em Redes e Infraestruturas de T.I e derivados, Nada mais é do que um Portscan (Scaneador de Portas) que realiza uma varredura no Host especificado em busca de Portas e Protocolos, Podendo ser util para o descobrimento de vulnerabilidades no seu Host/servidor, conseguindo identifica-las e posteriormente as corrigir (manualmente).

## Comandos:
> MODO DE UTILIZAR<br>
> /scan (alvo) -p (porta) -m (modo)<br>
> -----------------------------------------------------------------------<br>
> (alvo) - IP ou Domínio.<br>
> -----------------------------------------------------------------------<br>
> (porta) -> Portas ou Protocolo\n'
> Portas Especificas separar por Virgula (ex: 80,443,9050).<br>
> default - Scaneia as 30 principais portas.<br>
> all - Scaneia as 65536 portas, (Pode demorar um pouco).<br>
> -----------------------------------------------------------------------<br>
> (modo) -> Seleciona o timeout (Muito util).<br>
> fast - (0.2s de timeout) - Recomendado para REDES LOCAIS.<br>
> normal - (1s de timeout) - Recomendação PADRÃO.<br>
> slow - (3s de timeout) - Recomendado para PAGINAS WEB com respostas lenta<br><br>
> EXEMPLO<br>
> /scan seusite.com.br -p default -m normal<br>
>       ou 192.168.0.X<br>

> [!NOTE]
> Pode haver alguns BUGs, fique a vontade para modificar o arquivo e subir um PushRequest se necessario! (GLP 3.0)

> [!IMPORTANT]
> Se for gerar um executável com o Pyinstaller, certifique-se que o CSV esteja compactado junto com o EXE, ou que ele esteja na mesma pasta de execução do mesmo.
