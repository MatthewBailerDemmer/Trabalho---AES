import os
import numpy as np



s_box = [
    ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
    ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
    ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
    ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
    ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
    ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
    ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
    ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
    ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
    ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
    ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
    ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
    ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
    ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
    ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
    ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']
]

roundConstantTable = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']


print("Bem vindo ao cifrador/decifrador AES")

def expandirChaves():
    chaveExpandida = []
    chave = input("Foreça a chave em decimais seperados por vírgula (tamanho de chave 16 bytes) \n")
    numbers = list(map(int, chave.split(',')))
    
    #Vaida se a letra possi apenas 1 byte e transforma para hexadecimal
    for m in range(len(numbers)):
        if numbers[m] > 255:
            print("Decimal maior que 8 bits, chave inválida!")
            return False
        numbers[m] = numbers[m].to_bytes(1, byteorder='big').hex()
    
    #Valida tamnho de chave e realiza expansão PKCS#7
    if len(numbers) < 16:
        faltantes = 16 - len(numbers)
        for i in range(faltantes):
            numbers.append(faltantes)
    elif len(numbers) > 16:
        print("Tamanho de chave excedido")
        return None
    
    #Forma RoundKey 0
    roundKey = np.array(numbers).reshape((4, 4))
    
    chaveExpandida.append(roundKey)
    
    for z in range(10):
        #Geração de primeira palavra
        roundKeyAnterior = np.array(chaveExpandida[z])
        novaRoundKey = np.empty((4,4), dtype=object)
        # Etapa 1 e 2: Pega ultima palavra da roundKey anterior e rotaciona
        word1 = np.roll(roundKeyAnterior[3, :], -1)
        
        
        
        # Etapa 3: Substituir bytes (SubWord) com a s_box
        for byte in range(len(word1)):
            wordAux = str(word1[byte])
            linha = int(wordAux[0], 16)
            coluna = int(wordAux[1], 16)
            word1[byte] = s_box[linha][coluna]
            
        #Etapa 4: Geração da roundConstant
        roundConstant = [roundConstantTable[z], '00', '00', '00']
        
        #Etapa 5 fazendo XOR de palavra substituida e roundConstant (listComprehention)
        wordEtapa5 = np.array([f'{int(a, 16) ^ int(b, 16):02x}' for a, b in zip(word1, roundConstant)])
        
        #for h1, h2 in zip(word1, roundConstant):
         #   xor_result = int(h1, 16) ^ int(h2, 16)
          #  wordEtapa5.append(hex(xor_result))
        
        #Etapa 6: XOR entre primeira palavra da roundKey anterior e paravra etapa 5
        p_1_want = roundKeyAnterior[0, :]
        
        wordEtapa6 = np.array([f'{int(a, 16) ^ int(b, 16):02x}' for a, b in zip(p_1_want, wordEtapa5)])
        #for h1, h2 in zip(p_1_want, wordEtapa5):
         #   xor_result = int(h1, 16) ^ int(h2, 16)
          #  wordEtapa6.append(hex(xor_result))
    
        novaRoundKey[0] = wordEtapa6.tolist()
        
        #Gerando demais palavras da roundKey
        for i in range(1, 4):
            novaWord = np.array([f'{int(a, 16) ^ int(b, 16):02x}' for a, b in zip(roundKeyAnterior[i], novaRoundKey[i - 1])])
            
            #for h1, h2 in zip(roundKeyAnterior[i] ,novaRoundKey[i - 1]):
             #   xor_result = int(h1, 16) ^ int(h2, 16)
              #  novaWordAUx = hex(xor_result)
               # novaWordFormatada = str(novaWordAUx)[2:]
                #novaWord.append(novaWordFormatada)
            novaRoundKey[i] = novaWord.tolist()
            
        chaveExpandida.append(novaRoundKey)
    for i in chaveExpandida:
        print(i)
    
        
        


def cifrar():
    deuCerto = expandirChaves()
    if deuCerto == False:
        return None
    
    filePath = input("Forneça o caminho do arquivo a ser criptografado:")
    filePath = filePath.replace("\"", "")
    with open(filePath, 'rb') as file:
        contents = file.read()
        

def decifrar():
    deuCerto = expandirChaves()
    if deuCerto == False:
        return None
    
    print("Voce escolheu decifrar")







continuar = True
while continuar:
    opcao = input(f"Você deseja: \n1. Cifrar \n2. Decifrar \n3. Sair \n")
    if opcao == "1":
        cifrar()
    elif opcao == "2":
        decifrar()
    elif opcao == "3":
        print("Muito obrigado por utilizar o cifrador/decifrador AES")
        continuar = False
    else:
        print("Opção inválida!")
