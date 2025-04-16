import os
import shutil

#Troca de diretorio de arquivo para o desktop.
novoCaminho = r'C:\Users\sant\Desktop'
os.chdir(novoCaminho)


#verificando se a pasta 'cortesvideos' existe.
cortesVideos = os.path.exists('cortesvideos')


#caso não exista, faça a criação dela.
if not cortesVideos:
    novaPasta = os.mkdir('cortesvideos')
    print('Pasta criada com sucesso...')


#se já existir, perguntar se deseja excluir-la.
else:
    remocao = str(input(f'Deseja excluir a pasta de cortes? \n')).lower().strip()
    if remocao in 'ss' or remocao == 'sim':
        shutil.rmtree('cortesvideos')
        print('Pasta removida com sucesso.')

#verificando se a pasta 'cortesvideos' existe novamente.
cortesVideos = os.path.exists('cortesvideos')

#começar a produzir arquivos txt.
if cortesVideos == True:
    novoCaminho = r'C:\Users\sant\Desktop\cortesvideos'
    os.chdir(novoCaminho)
    with open('cortesVideosTexto', 'w') as arquivoTexto:
        arquivoTexto.write('Aqui será a pasta de cortes!!')
    with open('cortesVideosTexto', 'r') as arquivoTexto:
        conteudoArquivo = arquivoTexto.read()
        print(conteudoArquivo)


