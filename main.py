import os

print("Bem vindo ao cifrador/decifrador AES")


def cifrar():
    filePath = input("Forneça o caminho do arquivo a ser criptografado:")
    filePath = filePath.replace("\"", "")
    with open(filePath, 'rb') as file:
        contents = file.read()


def decifrar():
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
