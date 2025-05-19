import os
import numpy as np
import math
import base64



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

L = [
    ['00', '00', '01', '19', '02', '32', '1a', 'c6', '03', 'df', '33', 'ee', '1b', '68', 'c7', '4b'],
    ['04', '64', 'e0', '0e', '34', '8d', 'ef', '81', '1c', 'c1', '69', 'f8', 'c8', '08', '4c', '71'],
    ['05', '8a', '65', '2f', 'e1', '24', '0f', '21', '35', '93', '8e', 'da', 'f0', '12', '82', '45'],
    ['1d', 'b5', 'c2', '7d', '6a', '27', 'f9', 'b9', 'c9', '9a', '09', '78', '4d', 'e4', '72', 'a6'],
    ['06', 'bf', '8b', '62', '66', 'dd', '30', 'fd', 'e2', '98', '25', 'b3', '10', '91', '22', '88'],
    ['36', 'd0', '94', 'ce', '8f', '96', 'db', 'bd', 'f1', 'd2', '13', '5c', '83', '38', '46', '40'],
    ['1e', '42', 'b6', 'a3', 'c3', '48', '7e', '6e', '6b', '3a', '28', '54', 'fa', '85', 'ba', '3d'],
    ['ca', '5e', '9b', '9f', '0a', '15', '79', '2b', '4e', 'd4', 'e5', 'ac', '73', 'f3', 'a7', '57'],
    ['07', '70', 'c0', 'f7', '8c', '80', '63', '0d', '67', '4a', 'de', 'ed', '31', 'c5', 'fe', '18'],
    ['e3', 'a5', '99', '77', '26', 'b8', 'b4', '7c', '11', '44', '92', 'd9', '23', '20', '89', '2e'],
    ['37', '3f', 'd1', '5b', '95', 'bc', 'cf', 'cd', '90', '87', '97', 'b2', 'dc', 'fc', 'be', '61'],
    ['f2', '56', 'd3', 'ab', '14', '2a', '5d', '9e', '84', '3c', '39', '53', '47', '6d', '41', 'a2'],
    ['1f', '2d', '43', 'd8', 'b7', '7b', 'a4', '76', 'c4', '17', '49', 'ec', '7f', '0c', '6f', 'f6'],
    ['6c', 'a1', '3b', '52', '29', '9d', '55', 'aa', 'fb', '60', '86', 'b1', 'bb', 'cc', '3e', '5a'],
    ['cb', '59', '5f', 'b0', '9c', 'a9', 'a0', '51', '0b', 'f5', '16', 'eb', '7a', '75', '2c', 'd7'],
    ['4f', 'ae', 'd5', 'e9', 'e6', 'e7', 'e8', 'd6', '74', 'f4', 'ea', 'a8', '50', '8b', '5b', 'f9']
]

E = [
    ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36', '6c', 'd8', 'ab', '4d', '9a', '2f'],
    ['5e', 'bc', '63', 'c6', '97', '35', '6a', 'd4', 'b3', '7d', 'fa', 'ef', 'c5', '91', '39', '72'],
    ['e4', 'd3', 'bd', '61', 'c2', '9f', '25', '4a', '94', '33', '66', 'cc', '83', '1d', '3a', '74'],
    ['e8', 'cb', '8d', '01', '02', '04', '08', '10', '20', '40', '80', '1b', '36', '6c', 'd8', 'ab'],
    ['4d', '9a', '2f', '5e', 'bc', '63', 'c6', '97', '35', '6a', 'd4', 'b3', '7d', 'fa', 'ef', 'c5'],
    ['91', '39', '72', 'e4', 'd3', 'bd', '61', 'c2', '9f', '25', '4a', '94', '33', '66', 'cc', '83'],
    ['1d', '3a', '74', 'e8', 'cb', '8d', '01', '02', '04', '08', '10', '20', '40', '80', '1b', '36'],
    ['6c', 'd8', 'ab', '4d', '9a', '2f', '5e', 'bc', '63', 'c6', '97', '35', '6a', 'd4', 'b3', '7d'],
    ['fa', 'ef', 'c5', '91', '39', '72', 'e4', 'd3', 'bd', '61', 'c2', '9f', '25', '4a', '94', '33'],
    ['66', 'cc', '83', '1d', '3a', '74', 'e8', 'cb', '8d', '01', '02', '04', '08', '10', '20', '40'],
    ['80', '1b', '36', '6c', 'd8', 'ab', '4d', '9a', '2f', '5e', 'bc', '63', 'c6', '97', '35', '6a'],
    ['d4', 'b3', '7d', 'fa', 'ef', 'c5', '91', '39', '72', 'e4', 'd3', 'bd', '61', 'c2', '9f', '25'],
    ['4a', '94', '33', '66', 'cc', '83', '1d', '3a', '74', 'e8', 'cb', '8d', '01', '02', '04', '08'],
    ['10', '20', '40', '80', '1b', '36', '6c', 'd8', 'ab', '4d', '9a', '2f', '5e', 'bc', '63', 'c6'],
    ['97', '35', '6a', 'd4', 'b3', '7d', 'fa', 'ef', 'c5', '91', '39', '72', 'e4', 'd3', 'bd', '61'],
    ['c2', '9f', '25', '4a', '94', '33', '66', 'cc', '83', '1d', '3a', '74', 'e8', 'cb', '8d', '01'],
    ['02', '04', '08', '10', '20', '40', '80', '1b', '36', '6c', 'd8', 'ab', '4d', '9a', '2f', '5e'],
    ['bc', '63', 'c6', '97', '35', '6a', 'd4', 'b3', '7d', 'fa', 'ef', 'c5', '91', '39', '72', 'e4']
]


roundConstantTable = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']

matrizMult = [['02','03','01','01'],
              ['01','02','03','01'],
              ['01','01','02','03'],
              ['03','01','01','02']]


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
    for i in range(len(chaveExpandida)):
        chaveExpandida[i] = np.transpose(chaveExpandida[i])
    return chaveExpandida

def galoiMult(a, b):
    if a =='00' or b == '00':
        return '00'
    elif a == '01':
        return b
    elif b == '01':
        return a
    
    ra = L[int(a[0], 16)][int(a[1], 16)]
    rb = L[int(b[0], 16)][int(b[0], 16)]
    
    r = format(int(ra, 16) + int(rb,16), '02x')
    return E[int(r[0], 16)][int(r[1],16)]
    
    
    
    
        
 
def etapa4Cif(linha, coluna):
    mults = []
    for i, z in zip(linha, coluna):
        mults.append(galoiMult(i, z))
        
    result = 0
    for q in range(len(mults) - 1):
        result = f'{int(mults[q], 16) ^ int(mults[q + 1], 16):02x}'
    return result
        
        
         
            
        

def cifrar():
    chaveExpandida = expandirChaves()
    if chaveExpandida == False:
        return None
    
    filePath = input("Forneça o caminho do arquivo a ser criptografado:")
    filePath = filePath.replace("\"", "")
    #Lendo bytes arquivo e fazendo expansão pkcs#7 se necessário
    with open(filePath, 'rb') as file:
        contents = file.read()
        byte_list = [b for b in contents]
        nBytes = len(byte_list)
        
        #Verificando se o número de bytes é divisível por 16
        if nBytes % 16 != 0:
            if nBytes < 16:
                for g in range(16 - nBytes):
                    byte_list.append(16 - nBytes)
            else:
                nVezes = math.ceil(nBytes / 16)
                dif = 16 * nVezes - nBytes
                for g in range(dif):
                    byte_list.append(dif)
        
        # Dividindo a mensagem em blocos de 16
        blocos = []
        bloco = []
        for i in range(len(byte_list) + 1):
            if i % 16 == 0 and i != 0:
                blocoAux = np.array(bloco).reshape((4,4))
                blocoAux = np.transpose(blocoAux)
                blocos.append(blocoAux)
                bloco = []
            if i >= len(byte_list):
                break
            bloco.append(str(byte_list[i].to_bytes(1, byteorder='big').hex()))
        cifrado = []
        for bloquito in blocos:
            #Fazendo etapa 1: Xor com roundKey(0)
            int_matrix1 = np.vectorize(lambda x: int(x, 16))(bloquito)
            int_matrix2 = np.vectorize(lambda x: int(x, 16))(chaveExpandida[0])
            xor_result = np.bitwise_xor(int_matrix1, int_matrix2)
            etapa1 = np.vectorize(lambda x: format(x, '02x'))(xor_result)
            
            for r in range(1, 10):
                #Fazendo etapa 2: Subsituindo com s_box
                etapa2 = etapa1
                for byte in range(len(etapa2)):
                    for cx in range(len(etapa2[byte])):
                        wordAux = str(etapa2[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        etapa2[byte][cx] = s_box[linha][coluna]
                #Fazendo etapa 3: ShiftRows
                etapa3 = etapa2
                for z in range(len(etapa3)):
                    etapa3[z] = np.roll(etapa3[z, :], -z)
                #Fazendo etapa 4: MixColumns
                etapa4 = np.empty((4,4), dtype='U2')
                for p in range(etapa4.shape[0]):
                    for j in range(etapa4.shape[1]):
                        etapa4[p, j] = etapa4Cif(etapa3[:,j], matrizMult[p])
                        
                #Etapa 5: xor com RoundKey corrente
                etapa5 = etapa4
                int_matrix1 = np.vectorize(lambda x: int(x, 16))(etapa5)
                int_matrix2 = np.vectorize(lambda x: int(x, 16))(chaveExpandida[r])
                xor_result = np.bitwise_xor(int_matrix1, int_matrix2)
                etapa5 = np.vectorize(lambda x: format(x, '02x'))(xor_result)
                
               
            #Fazendo etapa 6: SubByte
            etapa6 = etapa5 
            for byte in range(len(etapa6)):
                    for cx in range(len(etapa6[byte])):
                        wordAux = str(etapa6[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        etapa6[byte][cx] = s_box[linha][coluna]
            #Fazendo etapa 7: ShiftRows
            etapa7 = etapa6
            for z in range(len(etapa7)):
                etapa7[z] = np.roll(etapa7[z, :], -z)
                
            #Etapa 8: xor com RoundKey corrente
            etapa8 = etapa7
            int_matrix1 = np.vectorize(lambda x: int(x, 16))(etapa8)
            int_matrix2 = np.vectorize(lambda x: int(x, 16))(chaveExpandida[10])
            xor_result = np.bitwise_xor(int_matrix1, int_matrix2)
            etapa8 = np.vectorize(lambda x: format(x, '02x'))(xor_result)
            
            cifrado.append(etapa8)
        stringResult = ""
        for i in cifrado:
            for x in i.T:
                for t in x:
                    stringResult += str(t)
                
        newFileName = input("Qual o nome do arquivo a guardar a criptografia resultante? (não esqueça a extensao)")
        
        with open(newFileName, 'w') as f:
            byte_datita = bytes.fromhex(stringResult)
            b64 = base64.b64encode(byte_datita)
            b64String = b64.decode('utf-8')
            f.write(b64String)
            
            
                
            
                
        
        

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
