 #!/usr/bin/env python3
# -- coding: utf-8 --
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem145101" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)
print("abriu com")

def server():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

     # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    stop = False
    bufferReceived = bytearray()
    while not stop:

        eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
        eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])

        head, headSize = com.getData(10)

        packageNumber = int.from_bytes(head[:3], "little")
        print ("Numero do pacote {}".format(packageNumber))
        totalPackage = int.from_bytes(head[3:6], "little")
        print ("Numero total de pacotes {}".format(totalPackage))
        payloadSize = int.from_bytes(head[9:], "little")
        print ("Tamnaho do payload {}".format(payloadSize))

        payloadEop, payloadEopSize = com.getData(int(payloadSize) + len(eop))
        if eop in payloadEop:
            i = payloadEop.find(eop)
            payload = payloadEop[:i]
            bufferReceived += payload
            print("EOP na posicão {}".format(i))

            if eop != payloadEop[i:]:
                print("ERRO: EOP está no lugar errado")
                com.sendData(bytes([0xa2]))
                print ("Transmitido {} bytes ".format(1))
                continue
        
        else: 
            print("ERRO: EOP não encontrado")
            com.sendData(bytes([0xa1]))
            print ("Transmitido {} bytes ".format(1))
            continue
        
        payload = payload.replace(eopReplaced, eop)

        payloadSize = len(payload)

        sizeReceived = payloadEopSize - len(eop)

        if sizeReceived == payloadSize:
            print("Sucesso")
            com.sendData(bytes([0xa3]))
            print ("Transmitido {} bytes ".format(1))
    
        print ("Recebidos {} bytes ".format(headSize + payloadEopSize))
        print(" ")

        if packageNumber == totalPackage:
            with open("testeee.jpg", "wb") as img:
                img.write(bufferReceived)
            stop = True

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    server()