# PortScanner Tool

![Screenshot 1](https://github.com/AlldDev/PortScanner-Tool/blob/main/assets/img_01.png)
![Screenshot 2](https://github.com/AlldDev/PortScanner-Tool/blob/main/assets/img_02.png)

---

## 💡 Sobre o Projeto

A **PortScanner Tool** é uma ferramenta simples, porém poderosa, para realizar varreduras de portas em redes e infraestruturas de T.I. O principal objetivo é auxiliar profissionais de suporte técnico e segurança em redes, permitindo identificar portas abertas e protocolos em hosts e servidores específicos.

Esta ferramenta pode ser usada para **descobrir vulnerabilidades** ou **monitorar a exposição de serviços**, oferecendo a capacidade de identificar possíveis falhas que podem ser corrigidas manualmente.

## 📋 Funcionalidades

- Realiza varredura de portas e protocolos em endereços IP ou domínios.
- Oferece diferentes modos de escaneamento (rápido, normal e lento) para otimização em diferentes cenários de rede.
- Varre portas específicas, principais portas ou todas as portas de um host.
- Pode ser usada para **auditoria de segurança** e **diagnóstico de rede**.

## ⚙️ Detalhes Técnicos

A ferramenta opera como um **scanner de portas** (port scan), investigando portas abertas e possíveis vulnerabilidades em um host/servidor especificado. A varredura de portas é um processo essencial em auditorias de segurança e monitoramento de rede, ajudando na identificação de serviços ativos e potencialmente expostos.

## 🔧 Comandos e Parâmetros

### Parâmetros Disponíveis

- **(alvo):** IP ou domínio a ser escaneado.
- **(porta):** Especifica as portas ou protocolo a serem escaneados.
  - Para portas específicas, separe por vírgula (ex: `80,443,9050`).
  - Para escanear as 30 principais portas, use `default`.
  - Para escanear todas as 65536 portas, use `all` (pode levar mais tempo).
  
- **(modo):** Define o tempo limite (timeout) para a varredura de portas.
  - **fast:** Timeout de 0.2s, recomendado para **redes locais**.
  - **normal:** Timeout de 0.5s, recomendação **padrão** para a maioria dos casos.
  - **slow:** Timeout de 2s, recomendado para **páginas web** ou redes com respostas mais lentas.

### Exemplo de Uso

```bash
/scan seusite.com.br -p default -m normal
```

## ⭐ Explicações Adicionais
O parâmetro (alvo) aceita tanto endereços IP quanto domínios. Certifique-se de inserir corretamente o alvo que deseja escanear.
Para o parâmetro (porta), você pode especificar portas individuais ou faixas de portas separadas por vírgula. Se usar default, serão escaneadas as 30 principais portas. Se usar all, serão escaneadas todas as 65536 portas (note que isso pode demorar mais).
O parâmetro (modo) ajusta o tempo limite (timeout) para cada porta escaneada. Escolha o modo que melhor se adeque à sua rede.
📄 Uso Ético
Esta ferramenta foi projetada para ser usada de maneira ética e responsável. Ao utilizar esta ferramenta, você deve:

Respeitar a privacidade: Não escaneie sistemas ou redes sem permissão explícita do proprietário.
Conformidade legal: Certifique-se de estar em conformidade com as leis e regulamentações locais e internacionais ao utilizar esta ferramenta.
Assumir responsabilidade: Você é o único responsável por qualquer uso desta ferramenta. Não a utilize para atividades maliciosas ou prejudiciais.

## 🚨 Avisos Importantes
 - Bugs e Sugestões: Pode haver alguns bugs. Sinta-se à vontade para modificar o código e enviar um Pull Request se encontrar melhorias.
 - PyInstaller: Se for gerar um executável com o PyInstaller, certifique-se de que o arquivo CSV esteja compactado junto com o executável, ou que ele esteja na mesma pasta de execução.

## 🔐 Segurança e Auditoria
Mantenha sempre sua rede monitorada com ferramentas de auditoria como esta para identificar portas abertas e serviços expostos.
Realize varreduras frequentes em servidores críticos para garantir que novas vulnerabilidades não apareçam devido a atualizações ou configurações incorretas.
Use firewalls e políticas de segurança adequadas para mitigar riscos após a identificação de portas vulneráveis.

## 📂 Licença
Este projeto está licenciado sob a GNU General Public License v3.0. Consulte o arquivo LICENSE.md para obter mais detalhes.
