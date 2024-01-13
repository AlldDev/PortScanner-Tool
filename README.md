# PortScanner Tool

![Screenshot ](https://github.com/AlldDev/PortScanner-Tool/blob/main/assets/portscanner_01.png)

![Screenshot ](https://github.com/AlldDev/PortScanner-Tool/blob/main/assets/portscanner_02.png)

Uma ferramenta simples para realizar varreduras de portas em redes e infraestruturas de T.I.

## Detalhes

A ferramenta foi desenvolvida com o objetivo de auxiliar o suporte em Redes e Infraestruturas de T.I. Ela funciona como um Portscan (Scanner de Portas), realizando varreduras em um host especificado em busca de portas e protocolos. Pode ser útil para descobrir vulnerabilidades em seu host/servidor, permitindo identificá-las e corrigi-las manualmente.

## Comandos

### Parâmetros
- **(alvo):** IP ou Domínio.
- **(porta):** Portas ou Protocolo. Para portas específicas, separar por vírgula (ex: 80,443,9050). Para escanear as 30 principais portas, use "default". Para escanear todas as 65536 portas, use "all".
- **(modo):** Seleciona o timeout.
  - **fast:** 0.2s de timeout, recomendado para REDES LOCAIS.
  - **normal:** 0.5s de timeout, recomendação PADRÃO.
  - **slow:** 2s de timeout, recomendado para PÁGINAS WEB com respostas lentas.

### Exemplo
/scan seusite.com.br -p default -m normal

### Explicações Adicionais
- O parâmetro **(alvo)** aceita tanto endereços IP quanto domínios. Certifique-se de inserir corretamente o alvo que deseja escanear.
- Para o parâmetro **(porta)**, você pode especificar portas individuais ou faixas de portas separadas por vírgula. Se usar "default", serão escaneadas as 30 principais portas. Se usar "all", serão escaneadas todas as 65536 portas (pode demorar).
- O parâmetro **(modo)** determina o tempo limite (timeout) para cada porta escaneada. Escolha o modo de acordo com a natureza da sua rede.

## Uso Ético

Esta ferramenta destina-se a ser usada de maneira ética e responsável. Ao usá-la, você concorda em:

1. **Respeitar a Privacidade:** Não use esta ferramenta para acessar informações sem permissão explícita.
2. **Conformidade Legal:** Certifique-se de estar em conformidade com todas as leis e regulamentações locais e internacionais ao utilizar esta ferramenta.
3. **Responsabilidade:** Você é o único responsável pelo uso desta ferramenta. Não a utilize para atividades maliciosas ou prejudiciais.

## Nota

Pode haver alguns bugs. Sinta-se à vontade para modificar o arquivo e enviar um Pull Request se necessário! (GLP 3.0)

## Importante

Se for gerar um executável com o Pyinstaller, certifique-se de que o CSV esteja compactado junto com o EXE, ou que ele esteja na mesma pasta de execução do mesmo.

## Licença

Este projeto está licenciado sob a [GNU General Public License v3.0](https://github.com/AlldDev/PortScanner-Tool/blob/main/LICENSE). Consulte o arquivo [LICENSE.md] para obter mais detalhes.
