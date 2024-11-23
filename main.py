import os
import subprocess
import traceback

# Caminhos principais
raiz = r"C:\Repositorios_GitHube\MeusProjetos\dividir_audio_faixas"
video_dir = os.path.join(raiz, "video")
output_dir = os.path.join(raiz, "Videos_Modificados")

# Certifique-se de que o diretório de saída existe
os.makedirs(output_dir, exist_ok=True)

def escolher_video(video_dir):
    """Permite ao usuário escolher um vídeo disponível."""
    videos = [f for f in os.listdir(video_dir) if f.endswith((".mp4", ".mkv", ".avi"))]
    
    if not videos:
        print("Nenhum vídeo encontrado na pasta!")
        return None
    
    print("Escolha o vídeo a ser processado:")
    for idx, video in enumerate(videos, 1):
        print(f"{idx}. {video}")
    
    escolha = int(input("Digite o número do vídeo escolhido: ")) - 1
    return os.path.join(video_dir, videos[escolha]) if 0 <= escolha < len(videos) else None

def extrair_audio(video_path, audio_path):
    """Extrai o áudio de um vídeo usando FFmpeg."""
    comando = [
        "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path
    ]
    subprocess.run(comando, check=True)

def exibir_span(mensagem, sucesso=True):
    """Exibe uma mensagem como span."""
    estilo = "background-color: green; color: white;" if sucesso else "background-color: red; color: white;"
    print(f"<span style='{estilo}'>{mensagem}</span>")

def processar_video(video_path, output_dir):
    """Processa um único vídeo."""
    nome_base = os.path.splitext(os.path.basename(video_path))[0]
    pasta_saida = os.path.join(output_dir, nome_base)
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_audio = os.path.join(pasta_saida, f"{nome_base}_audio.wav")
    
    try:
        # Extrair áudio do vídeo
        extrair_audio(video_path, caminho_audio)
        exibir_span("O áudio foi extraído com sucesso, podemos fazer a separação?", sucesso=True)
        
        # Separar faixas de áudio usando Demucs
        comando_demucs = [
            "demucs",
            "-n", "htdemucs",  # Modelo de separação
            "--out", pasta_saida,  # Pasta de saída
            caminho_audio
        ]
        subprocess.run(comando_demucs, check=True)
        exibir_span("As faixas de áudio foram separadas com sucesso!", sucesso=True)
        print(f"Processamento concluído para: {video_path}")
    except subprocess.CalledProcessError as e:
        linha_erro = traceback.extract_tb(e.__traceback__)[-1].lineno
        erro_tecnico = str(e)
        exibir_span(f"O vídeo não foi processado, erro na linha {linha_erro}, por conta de {erro_tecnico}", sucesso=False)
    except Exception as e:
        linha_erro = traceback.extract_tb(e.__traceback__)[-1].lineno
        erro_tecnico = str(e)
        exibir_span(f"O vídeo não foi processado, erro na linha {linha_erro}, por conta de {erro_tecnico}", sucesso=False)

# Executar o script
video_path = escolher_video(video_dir)
if video_path:
    processar_video(video_path, output_dir)
