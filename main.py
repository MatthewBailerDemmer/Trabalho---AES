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

inv_s_box = [
    ['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'],
    ['7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'],
    ['54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'],
    ['08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'],
    ['72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'],
    ['6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'],
    ['90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'],
    ['D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'],
    ['3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'],
    ['96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E'],
    ['47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'],
    ['FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'],
    ['1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'],
    ['60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'],
    ['A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61'],
    ['17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D']
]

L = [
    ["00", "00", "19", "01", "32", "02", "1a", "c6", "4b", "c7", "1b", "68", "33", "ee", "df", "03"],
    ["64", "04", "e0", "0e", "34", "8d", "81", "ef", "4c", "71", "08", "c8", "f8", "69", "1c", "c1"],
    ["7d", "c2", "1d", "b5", "f9", "b9", "27", "6a", "4d", "e4", "a6", "72", "9a", "c9", "09", "78"],
    ["65", "2f", "8a", "05", "21", "0f", "e1", "24", "12", "f0", "82", "45", "35", "93", "da", "8e"],
    ["96", "8f", "db", "bd", "36", "d0", "ce", "94", "13", "5c", "d2", "f1", "40", "46", "83", "38"],
    ["66", "dd", "fd", "30", "bf", "06", "8b", "62", "b3", "25", "e2", "98", "22", "88", "91", "10"],
    ["7e", "6e", "48", "c3", "a3", "b6", "1e", "42", "3a", "6b", "28", "54", "fa", "85", "3d", "ba"],
    ["2b", "79", "0a", "15", "9b", "9f", "5e", "ca", "4e", "d4", "ac", "e5", "f3", "73", "a7", "57"],
    ["af", "58", "a8", "50", "f4", "ea", "d6", "74", "4f", "ae", "e9", "d5", "e7", "e6", "ad", "e8"],
    ["2c", "d7", "75", "7a", "eb", "16", "0b", "f5", "59", "cb", "5f", "b0", "9c", "a9", "51", "a0"],
    ["7f", "0c", "f6", "6f", "17", "c4", "49", "ec", "d8", "43", "1f", "2d", "a4", "76", "7b", "b7"],
    ["cc", "bb", "3e", "5a", "fb", "60", "b1", "86", "3b", "52", "a1", "6c", "aa", "55", "29", "9d"],
    ["97", "b2", "87", "90", "61", "be", "dc", "fc", "bc", "95", "cf", "cd", "37", "3f", "5b", "d1"],
    ["53", "39", "84", "3c", "41", "a2", "6d", "47", "14", "2a", "9e", "5d", "56", "f2", "d3", "ab"],
    ["44", "11", "92", "d9", "23", "20", "2e", "89", "b4", "7c", "b8", "26", "77", "99", "e3", "a5"],
    ["67", "4a", "ed", "de", "c5", "31", "fe", "18", "0d", "63", "8c", "80", "c0", "f7", "70", "07"]
]

E = [
    ["01", "03", "05", "0f", "11", "33", "55", "ff", "1a", "2e", "72", "96", "a1", "f8", "13", "35"],
    ["5f", "e1", "38", "48", "d8", "73", "95", "a4", "f7", "02", "06", "0a", "1e", "22", "66", "aa"],
    ["e5", "34", "5c", "e4", "37", "59", "eb", "26", "6a", "be", "d9", "70", "90", "ab", "e6", "31"],
    ["53", "f5", "04", "0c", "14", "3c", "44", "cc", "4f", "d1", "68", "b8", "d3", "6e", "b2", "cd"],
    ["4c", "d4", "67", "a9", "e0", "3b", "4d", "d7", "62", "a6", "f1", "08", "18", "28", "78", "88"],
    ["83", "9e", "b9", "d0", "6b", "bd", "dc", "7f", "81", "98", "b3", "ce", "49", "db", "76", "9a"],
    ["b5", "c4", "57", "f9", "10", "30", "50", "f0", "0b", "1d", "27", "69", "bb", "d6", "61", "a3"],
    ["fe", "19", "2b", "7d", "87", "92", "ad", "ec", "2f", "71", "93", "ae", "e9", "20", "60", "a0"],
    ["fb", "16", "3a", "4e", "d2", "6d", "b7", "c2", "5d", "e7", "32", "56", "fa", "15", "3f", "41"],
    ["c3", "5e", "e2", "3d", "47", "c9", "40", "c0", "5b", "ed", "2c", "74", "9c", "bf", "da", "75"],
    ["9f", "ba", "d5", "64", "ac", "ef", "2a", "7e", "82", "9d", "bc", "df", "7a", "8e", "89", "80"],
    ["9b", "b6", "c1", "58", "e8", "23", "65", "af", "ea", "25", "6f", "b1", "c8", "43", "c5", "54"],
    ["fc", "1f", "21", "63", "a5", "f4", "07", "09", "1b", "2d", "77", "99", "b0", "cb", "46", "ca"],
    ["45", "cf", "4a", "de", "79", "8b", "86", "91", "a8", "e3", "3e", "42", "c6", "51", "f3", "0e"],
    ["12", "36", "5a", "ee", "29", "7b", "8d", "8c", "8f", "8a", "85", "94", "a7", "f2", "0d", "17"],
    ["39", "4b", "dd", "7c", "84", "97", "a2", "fd", "1c", "24", "6c", "b4", "c7", "52", "f6", "01"]
]


roundConstantTable = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']

matrizMult = [['02','03','01','01'],
              ['01','02','03','01'],
              ['01','01','02','03'],
              ['03','01','01','02']]

matrixMultInv = [['0e', '0b', '0d', '09'],
                 ['09', '0e', '0b', '0d'],
                 ['0d', '09', '0e', '0b'],
                 ['0b', '0d', '09', '0e']]


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
   if a == '00' or b == '00':
       return '00'
   elif a == 1:
       return b
   elif b == 1:
       return a
   
   linha = int(a[0], 16)
   coluna = int(a[1], 16)
   La = L[linha][coluna]
   
   linha = int(b[0], 16)
   coluna = int(b[1], 16)
   Lb = L[linha][coluna]
   result = int(La, 16) + int(Lb, 16)
   if result > 255:
       result = result - 255
    
   resE = f'{result:02x}'
   linha = int(resE[0], 16)
   coluna = int(resE[1], 16)
   resE = E[linha][coluna]
   
   return resE
   
   
   
    
    
    
    
        
 
def etapa4Cif(coluna, linha):
    mults = []
    for i, z in zip(coluna, linha):
        mults.append(galoiMult(i, z))
    result = f'{int(mults[0], 16) ^ int(mults[1], 16) ^ int(mults[2], 16) ^ int(mults[3], 16):02x}' 
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
        byte_list = [f'{byte:02x}' for byte in contents]
        nBytes = len(byte_list)
        
        #Verificando se o número de bytes é divisível por 16
        if nBytes % 16 != 0:
            if nBytes < 16:
                for g in range(16 - nBytes):
                    byte_list.append(f"{16 - nBytes:02x}")
            else:
                #PKCS#7
                nVezes = math.ceil(nBytes / 16)
                dif = 16 * nVezes - nBytes
                for g in range(dif):
                    byte_list.append(f"{dif:02x}")
        
        # Dividindo a mensagem em blocos de 16
        blocos = []
        bloco = []
        while len(byte_list) != 0:
             bloco.append(byte_list[0])
             byte_list = byte_list[1:]
             if len(bloco) % 16 == 0:
                blocoAux = np.array(bloco).reshape((4,4))
                blocoAux = np.transpose(blocoAux)
                blocos.append(blocoAux)
                bloco = []
        
        
        cifrado = []
        for bloquito in blocos:
            #Fazendo etapa 1: Xor com roundKey(0)
            for i in range(len(bloquito)):
                for z in range(len(bloquito[i])):
                    bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[0][i][z], 16):02x}'
            
            for r in range(10):
                #Fazendo etapa 2: Subsituindo com s_box
                for byte in range(len(bloquito)):
                    for cx in range(len(bloquito[byte])):
                        wordAux = str(bloquito[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        bloquito[byte][cx] = s_box[linha][coluna]
                #Fazendo etapa 3: ShiftRows
                for z in range(len(bloquito)):
                    bloquito[z] = np.roll(bloquito[z], -z)
                #Fazendo etapa 4: MixColumns
                #for p in range(len(bloquito)):
                #    for j in range(len(bloquito[p])):
                #        bloquito[p, j] = etapa4Cif(bloquito[:, j], matrizMult[p])
                        
                #Etapa 5: xor com RoundKey corrente
                if r > 9:
                    for i in range(len(bloquito)):
                        for z in range(len(bloquito[i])):
                            bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[r + 1][i][z], 16):02x}'
                
               
            #Fazendo etapa 6: SubByte
            for byte in range(len(bloquito)):
                    for cx in range(len(bloquito[byte])):
                        wordAux = str(bloquito[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        bloquito[byte][cx] = s_box[linha][coluna]
            
            #Fazendo etapa 7: ShiftRows
            for z in range(len(bloquito)):
                bloquito[z] = np.roll(bloquito[z, :], -z)
                
            #Etapa 8: xor com RoundKey 11
            for i in range(len(bloquito)):
                    for z in range(len(bloquito[i])):
                        bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[10][i][z], 16):02x}'
            
            cifrado.append(bloquito)
            
        cifrado = np.array(cifrado)
        
        stringResult = ""
        for i in cifrado:
            for x in i.T:
                for t in x:
                    stringResult += str(t)
        newFileName = input("Qual o nome do arquivo a guardar a criptografia resultante? (não esqueça a extensao)")
        
        with open(newFileName, 'w') as f:
            f.write(stringResult)
            
            
                
            
                
        
        

def decifrar():
    chaveExpandida = expandirChaves()
    if chaveExpandida == False:
        return None
    
    filePath = input("Forneça o caminho do arquivo a ser decifrado:")
    filePath = filePath.replace("\"", "")
    
    with open(filePath, 'r') as file:
        contents = file.read()
        byte_list = []
        for i in range(len(contents) - 1):
            byte_list.append(f'{contents[i] + contents[i + 1]}')
        nBytes = len(byte_list)
        
        # Dividindo a mensagem em blocos de 16
        blocos = []
        bloco = []
        while len(contents) != 0:
             bloco.append(f'{contents[0] + contents[1]}')
             contents = contents[2:]
             if len(bloco) % 16 == 0:
                blocoAux = np.array(bloco).reshape((4,4))
                blocoAux = np.transpose(blocoAux)
                blocos.append(blocoAux)
                bloco = []
            
            
        
        
        cifrado = []
        for bloquito in blocos:
            #Fazendo etapa 1: Xor com roundKey(0)
            for i in range(len(bloquito)):
                for z in range(len(bloquito[i])):
                    bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[10][i][z], 16):02x}'
                    
            #Fazendo etapa2: InvShifRows
            for z in range(len(bloquito)):
                bloquito[z] = np.roll(bloquito[z], z)
                
            #Fazendo etapa3: InvSubBytes
            for byte in range(len(bloquito)):
                    for cx in range(len(bloquito[byte])):
                        wordAux = str(bloquito[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        bloquito[byte][cx] = inv_s_box[linha][coluna]
            
            for r in range(10):
            #Fazendo etapa4: RoundKey round
                if r > 9:
                    for i in range(len(bloquito)):
                        for z in range(len(bloquito[i])):
                            bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[r][i][z], 16):02x}'
            #Fazendo etapa5: InvMixColumns
                #for p in range(len(bloquito)):
                #    for j in range(len(bloquito[p])):
                #        bloquito[p, j] = etapa4Cif(bloquito[:, j], matrixMultInv[p])
            
            #Fazendo etapa6: InvShiftRows
                for z in range(len(bloquito)):
                    bloquito[z] = np.roll(bloquito[z], z)
                    
                #Fazendo etapa7: InvSubBytes
                for byte in range(len(bloquito)):
                    for cx in range(len(bloquito[byte])):
                        wordAux = str(bloquito[byte][cx])
                        linha = int(wordAux[0], 16)
                        coluna = int(wordAux[1], 16)
                        bloquito[byte][cx] = inv_s_box[linha][coluna]
            
            #Fazendo etapa8: RoundKey[0]
            for i in range(len(bloquito)):
                for z in range(len(bloquito[i])):
                    bloquito[i][z] = f'{int(bloquito[i][z], 16) ^ int(chaveExpandida[0][i][z], 16):02x}'
            
            cifrado.append(bloquito)
        
        cifrado = np.array(cifrado)
        stringResult = ""
        for i in cifrado:
            for x in i.T:
                for t in x:
                    stringResult += bytes.fromhex(t).decode('ascii')
                
        newFileName = input("Qual o nome do arquivo a guardar o conteudo descriptografado resultante? (não esqueça a extensao)")
        
        with open(newFileName, 'w') as f:
            f.write(stringResult)
                
            
                
                
            
            
        






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
