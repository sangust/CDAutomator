import os
import re
import sys
import getpass
import yt_dlp
import moviepy
import moviepy.config as mpc  # MÓDULO CORRETO PARA CONFIGURAR FFMPEG
from zipfile import ZipFile, ZIP_DEFLATED
from moviepy.video.io.VideoFileClip import VideoFileClip



#CONFIGURAÇÕES DO SISTEMA
def solicitar_url():
    url = str(input('\nDigite a URL do video para criar os cortes!\nCaso deseje sair do programa, digite sair\n'))
    if url == 'sair':
        sys.exit('Você saiu do software...')
    return url

def nome_seguro(nome):
    return re.sub(r'[\\/*?:"<>|.]', "", nome)
    
def obter_caminho_videos():
    usuario = getpass.getuser()
    pasta_downloads = os.path.join('C:\\Users', usuario, 'Downloads')
    return pasta_downloads

def pasta_zipada(pasta_donwloads):
    pasta_para_zipar = os.listdir(pasta_donwloads)
    
    for arquivos in pasta_para_zipar:
        sem_extensao = arquivos.split('.')[0]
        nome_zip = os.path.join(pasta_donwloads, sem_extensao + '.zip')
        arquivo_zip = ZipFile(nome_zip, "w", compression=ZIP_DEFLATED)
        arquivo_zip.write(os.path.join(pasta_donwloads, arquivos), arquivos)



# ========== CONFIGURAÇÃO FFMPEG ==========
def configurar_ffmpeg():
    if hasattr(sys, '_MEIPASS'):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FFMPEG_BINARY = os.path.join(BASE_DIR, 'ffmpeg', 'ffmpeg.exe')
    FFPROBE_BINARY = os.path.join(BASE_DIR, 'ffmpeg', 'ffprobe.exe')
    mpc.FFMPEG_BINARY = FFMPEG_BINARY
    mpc.FFPROBE_BINARY = FFPROBE_BINARY


# Detecta o diretório base para acesso ao ffmpeg e ffprobe, mesmo em modo empacotado (PyInstaller)
def baixar_stream(stream, filename):
    try:
        stream.download(filename=filename)
    except Exception as e:
        print(f"Erro ao baixar {filename}: {e}")


def baixar_videoaudio(Pasta_downloads):
    url = solicitar_url()
    info_temp = None

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl_temp:
            info_temp = ydl_temp.extract_info(url, download=False)
    except Exception as e:
        print(f"\n❌ Erro ao obter informações do vídeo: {e}")
        return None

    nome_limpo = nome_seguro(info_temp.get('title', 'video'))
    pasta_video_cortes = os.path.join(Pasta_downloads, nome_limpo)
    os.makedirs(pasta_video_cortes, exist_ok=True)
    outtmpl_fixo = os.path.join(pasta_video_cortes, f'{nome_limpo}.%(ext)s')

    opcoes = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': outtmpl_fixo,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            nome_arquivo = ydl.prepare_filename(info)
            print(f"\n✅ Download finalizado: {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            print(f"\n❌ Erro ao baixar o vídeo: {e}")
            return None
    


#cortes do video.#inicio do clipe = i, começa em 0, dps 120, 240...
def cortes_videos(caminho_mp4):
    if not caminho_mp4 or not os.path.isfile(caminho_mp4):
        print('Arquivo de vídeo inválido.')
        return
    
    diretorio = os.path.dirname(caminho_mp4) 
    os.chdir(diretorio) 

    nome_arquivo = os.path.basename(caminho_mp4)
    video_final = VideoFileClip(nome_arquivo)
    duracao_video = video_final.duration
    duracao_cortes = 120
    nome_corte = 1

    for i in range(0, int(duracao_video), duracao_cortes):
        inicio = i
        fim = min(inicio + duracao_cortes, duracao_video)
        corte = video_final.subclipped(inicio, fim)
        nome_arquivo = f'corte_{nome_corte}.mp4'
        corte.write_videofile(nome_arquivo, codec='libx264')
        nome_corte += 1



#menu de seleção
def menu_software():
    menu_escolha = 0
    while menu_escolha not in ['1', '2', '3']:
        menu_escolha = input('\nEscolha a opção desejada a seguir:\n[1] -> Deseja iniciar o software do zero?\n[2] -> Criação ou remoção da pasta de cortes\n[3] -> Download do video e automatização dos cortes\n')
        if menu_escolha in ['1', '2', '3']:
            break
        else:
            print('ERROR!! ERROR!!\nSelecione 1, 2 ou 3, tenha certeza que esteja dentro dos parametros...')
    return menu_escolha






def readme(Pasta_CDA_Existe):
    os.chdir(Pasta_CDA_Existe)
    with open('CDA.ReadMe', 'w') as arquivoTexto:
        arquivoTexto.write('Este é um Software baseado em automatizar contas darks nas redes, majoritariamente no tiktok, instagram, e youtube shorts'
        'para utilizar-lo, você deve copiar a URL/Link de um video do youtube (podcasts, gameplays, etc...) e colar no programa'
        'após isso, o software irá criar um diretorio principal, e varios subdiretorios com o titulo dos videos baixados, dentro de cada'
        'subdiretorio haverá os cortes do video especificado.')






def main():
    pasta_CDA_existe = criar_verificar_pastas()
    nome_arquivo_video = baixar_videoaudio(pasta_CDA_existe)
    readme(pasta_CDA_existe)
    cortes_videos(nome_arquivo_video)
    

def main_pastacortes():
    pasta_CDA_existe = criar_verificar_pastas()
    readme(pasta_CDA_existe)


def main_baixarvideos():
    Pasta_CDA_Existe = obter_caminho()
    nome_arquivo_video = baixar_videoaudio(Pasta_CDA_Existe)
    cortes_videos(nome_arquivo_video)    
    

menu = menu_software()
if menu == '1':
        main() 
elif menu == '2':
        main_pastacortes()
elif menu == '3':
        main_baixarvideos()