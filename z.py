from scapy.all import sniff

# Função de callback que será chamada para cada pacote capturado


def packet_callback(packet):
    # Aqui você pode processar os pacotes conforme necessário
    print(packet.summary())

# Função principal que inicia a captura de pacotes


def main():
    # O argumento iface define a interface de rede que você deseja monitorar
    # O filtro pode ser usado para filtrar tipos específicos de pacotes (usando a sintaxe BPF)
    # Exemplo: "tcp", "udp", "icmp", etc.
    # iface='eth0' pode ser necessário dependendo do seu sistema e interface de rede
    sniff(prn=packet_callback, store=0)


if __name__ == '__main__':
    main()
