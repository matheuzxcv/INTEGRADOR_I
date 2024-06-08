import pygame
import random
import sys
import serial
import time
from gtts import gTTS
import os
import threading
pygame.init()

# Definindo algumas cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Definindo as configurações da janela
WIDTH, HEIGHT = 989, 655
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60

palavra = ['0', '0', '0', '0', '0', '0']
# Inicializando o Pygame

# Criando a janela do jogo
screen = pygame.display.set_mode(WINDOW_SIZE)
imagem_fundo = pygame.image.load("./imagens/fu.png")
pygame.display.set_caption("Digite a Palavra")

# Carregando a fonte
font = pygame.font.Font("./fontes/Welcome-Magic.ttf", 80)

# Carregando sons
acerto_som = pygame.mixer.Sound("./sons/correct.mp3")
erro_som = pygame.mixer.Sound("./sons/error.mp3")

# Lista de imagens
image_path_banana = "./imagens/bananaa.png"
image_banana = pygame.image.load(image_path_banana)
image_banana = pygame.transform.scale(image_banana, (300, 150))

image_path_sol = "./imagens/sool.png"
image_sol = pygame.image.load(image_path_sol)
image_sol = pygame.transform.scale(image_sol, (300, 150))

image_path_cachorro = "./imagens/cachorro.png"
image_cachorro = pygame.image.load(image_path_cachorro)
image_cachorro = pygame.transform.scale(image_cachorro, (300, 150))

image_path_gato = "./imagens/gato.png"
image_gato = pygame.image.load(image_path_gato)
image_gato = pygame.transform.scale(image_gato, (300, 150))

image_path_carro = "./imagens/carro.png"
image_carro = pygame.image.load(image_path_carro)
image_carro = pygame.transform.scale(image_carro, (300, 150))

image_path_lapis = "./imagens/lapis.png"
image_lapis = pygame.image.load(image_path_lapis)
image_lapis = pygame.transform.scale(image_lapis, (300, 150))

image_path_bolas = "./imagens/bolas.png"
image_bolas = pygame.image.load(image_path_bolas)
image_bolas = pygame.transform.scale(image_bolas, (300, 150))

image_path_radio = "./imagens/radio.png"
image_radio = pygame.image.load(image_path_radio)
image_radio = pygame.transform.scale(image_radio, (300, 150))

image_path_amor = "./imagens/amor.png"
image_amor = pygame.image.load(image_path_amor)
image_amor = pygame.transform.scale(image_amor, (300, 150))

image_path_comer = "./imagens/comer.png"
image_comer = pygame.image.load(image_path_comer)
image_comer = pygame.transform.scale(image_comer, (300, 150))

image_path_nadar = "./imagens/nadar.png"
image_nadar = pygame.image.load(image_path_nadar)
image_nadar = pygame.transform.scale(image_nadar, (300, 150))

image_path_casar = "./imagens/casar.png"
image_casar = pygame.image.load(image_path_casar)
image_casar = pygame.transform.scale(image_casar, (300, 150))

image_path_pular = "./imagens/pular.png"
image_pular = pygame.image.load(image_path_pular)
image_pular = pygame.transform.scale(image_pular, (300, 150))

image_path_rato = "./imagens/rato.png"
image_rato = pygame.image.load(image_path_rato)
image_rato = pygame.transform.scale(image_rato, (300, 150))

image_path_linha = "./imagens/linha.png"
image_linha = pygame.image.load(image_path_linha)
image_linha = pygame.transform.scale(image_linha, (300, 150))

# Lista de palavras e imagens
dicio = {
    "banana": image_banana,
    "sol": image_sol,
    "cachorro": image_cachorro,
    "gato": image_gato,
    "carro": image_carro,
    "lapis": image_lapis,
    "bolas": image_bolas,
    "radio": image_radio,
    "amor": image_amor,
    "comer": image_comer,
    "nadar": image_nadar,
    "casar": image_casar,
    "pular": image_pular,
    "rato": image_rato,
    "linha": image_linha
}
palavras = list(dicio.keys())

# Posições das letras faltantes
posicoes = {
    "banana": [4, 5],
    "sol": [1, 2],
    "cachorro": [5, 6],
    "gato": [1, 3],
    "carro": [2, 3],
    "lapis": [0, 1],
    "bolas": [0, 1],
    "radio": [0, 1],
    "amor": [2, 3],
    "comer": [0, 1],
    "nadar": [0, 1],
    "casar": [2, 3],
    "pular": [2, 3],
    "rato": [0, 1],
    "linha": [0, 1]
}

# Criar diretório de áudios, se não existir
if not os.path.exists('audios'):
    os.makedirs('audios')

# Função para criar áudio da palavra
def criar_audio(palavra):
    tts = gTTS(text=palavra, lang='pt-br')  # Muda a voz para português do Brasil
    filename = os.path.join('audios', f"{palavra}.mp3")
    tts.save(filename)
    return filename

# Função para tocar áudio da palavra
def tocar_audio(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Erro ao tocar áudio: {e}")

# Variável global para rastrear a palavra atual
indice_palavra = 0

# Função para exibir a próxima palavra na lista
def proxima_palavra():
    global indice_palavra
    palavra = palavras[indice_palavra]
    palavra_modificada = list(palavra)
    letras_faltantes = []
    for pos in posicoes[palavra]:
        letras_faltantes.append(palavra[pos])
        palavra_modificada[pos] = '_'
    indice_palavra = (indice_palavra + 1) % len(palavras)
    return "".join(palavra_modificada), letras_faltantes, palavra

# Função para desenhar o texto na tela
def desenhar_texto(texto, x, y, cor=BLACK):
    texto_surface = font.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(center=(x, y))
    screen.blit(texto_surface, texto_rect)

def monta_palavra(posicao, caractere):
    indices_validos = {'0', '1', '2', '3', '4', '5'}
    if posicao in indices_validos:
        palavra[int(posicao)] = caractere
    else:
        print("Erro na montagem de palavras")

def leitura_caracteres():
    input_text = ""
    while len(input_text) < 2:
        received_char = ser.read().decode('utf-8').strip()
        if received_char:
            input_text += received_char.lower()
    return input_text[0], input_text[1]

def filtra_palavra(palavra):
    return ''.join([char for char in palavra if char != '0'])

def limpar():
    global palavra
    palavra = ['0', '0', '0', '0', '0', '0']


# Configurações da porta serial
port = '/dev/ttyUSB0'  # Ajuste conforme necessário
baud_rate = 9600

try:
    ser = serial.Serial(port, baud_rate, timeout=0.1)
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")
    sys.exit(1)

# Função principal do jogo
# Função principal do jogo
def main():
    palavra_atual, letras_faltando, palavra_completa = proxima_palavra()
    input_text = ""
    palavra_filtrada = ""
    
    score = 0
    mostrar_palavra_completa = False

    # Criar e tocar áudio da palavra
    audio_file = criar_audio(palavra_completa)
    tocar_audio(audio_file)

    clock = pygame.time.Clock()
    running = True


    try:
        while running:
            screen.blit(imagem_fundo, (0, 0))

            # Desenha a palavra atual na tela com '_'
            desenhar_texto(palavra_atual, WIDTH // 2, HEIGHT // 1.7)

            # Desenha o texto de entrada na tela
            desenhar_texto(input_text, WIDTH // 2, HEIGHT // 2 + 10)

            # Desenha a pontuação na tela
            desenhar_texto(f"Score: {score}", WIDTH // 2, 50)

            # Desenha a imagem correspondente
            screen.blit(dicio[palavra_completa], (WIDTH / 3, HEIGHT // 4))

            # Se necessário, desenha a palavra completa abaixo da imagem

            pygame.display.flip()

            # Verifica eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            # Leitura da entrada serial
            if ser.in_waiting > 0:
                posicao, caractere = leitura_caracteres()
                monta_palavra(posicao, caractere)
                palavra_filtrada = filtra_palavra(palavra)
                #received_char = ser.read().decode('utf-8').strip()
                if len(palavra_filtrada) < 2:  # Limita a entrada a duas letras
                    desenhar_texto(palavra_filtrada, WIDTH // 2, HEIGHT // 2 + 10)
                    pygame.display.flip()
                # Verifica se a entrada está completa
                if len(palavra_filtrada) == 2:
                    if sorted(palavra_filtrada) == sorted(letras_faltando):
                        score += 1
                        acerto_som.play()
                        desenhar_texto(palavra_completa, WIDTH // 2, HEIGHT // 2 + 150)  # Desenha a palavra completa após o acerto
                        pygame.display.flip()  # Atualiza a tela
                        time.sleep(1)  # Dá um delay
                        tocar_audio(audio_file)  # Toca a palavra completa
                        time.sleep(2)  # Dá um delay
                        palavra_filtrada = ""
                        limpar()
                        # Gera uma nova palavra após acerto
                        palavra_atual, letras_faltando, palavra_completa = proxima_palavra()
                        # Criar e tocar áudio da nova palavra
                        audio_file = criar_audio(palavra_completa)
                        tocar_audio(audio_file)
                        
                        pygame.display.flip()
                    else:
                        erro_som.play()
                        # Mantém a mesma palavra após erro
                        palavra_filtrada = ""
                        limpar()
            
            
            clock.tick(FPS)

    finally:
        # Fechar o Pygame e a porta serial
        pygame.quit()
        ser.close()

if __name__ == "__main__":
    main()
