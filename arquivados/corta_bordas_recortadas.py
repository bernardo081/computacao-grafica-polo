import os
from PIL import Image

# Pasta origem com as imagens
folder_path = "metades_recortadas_finais"

# Pasta destino para salvar a imagem concatenada
output_folder = "paginas_completas"

# Cria a pasta destino se não existir
os.makedirs(output_folder, exist_ok=True)

# Lista para armazenar os caminhos das imagens na ordem correta
imagens_ordenadas = []

# Primeiro, coleta todas as imagens e extrai os números das páginas
arquivos_paginas = []

for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        # Extrai o número da página do nome do arquivo
        partes = filename.split('_')
        if len(partes) >= 3 and partes[2].isdigit():
            numero_pagina = int(partes[2])
            arquivos_paginas.append((numero_pagina, filename))

# Ordena as páginas pelo número
arquivos_paginas.sort(key=lambda x: x[0])

# Agora organiza na ordem: esquerda1, direita1, esquerda2, direita2, etc.
for numero, filename in arquivos_paginas:
    if "esquerda" in filename:
        # Encontra a correspondente direita
        correspondente_direita = None
        for num2, filename2 in arquivos_paginas:
            if num2 == numero and "direita" in filename2:
                correspondente_direita = filename2
                break
        
        if correspondente_direita:
            imagens_ordenadas.append(os.path.join(folder_path, filename))
            imagens_ordenadas.append(os.path.join(folder_path, correspondente_direita))

# Cria a imagem gigante concatenada
if imagens_ordenadas:
    # Abre a primeira imagem para obter as dimensões
    primeira_imagem = Image.open(imagens_ordenadas[0])
    largura = primeira_imagem.width
    
    # Calcula a altura total
    altura_total = 0
    imagens_abertas = []
    
    for caminho_imagem in imagens_ordenadas:
        img = Image.open(caminho_imagem)
        imagens_abertas.append(img)
        altura_total += img.height
    
    # Cria a nova imagem com altura total
    nova_imagem = Image.new('RGB', (largura, altura_total))
    
    # Cola todas as imagens verticalmente
    y_offset = 0
    for img in imagens_abertas:
        nova_imagem.paste(img, (0, y_offset))
        y_offset += img.height
        img.close()  # Fecha a imagem para liberar memória
    
    # Salva a imagem concatenada
    output_path = os.path.join(output_folder, "todas_paginas_concatenadas.png")
    nova_imagem.save(output_path)
    
    print(f"Imagem gigante criada com sucesso!")
    print(f"Total de {len(imagens_ordenadas)} imagens concatenadas")
    print(f"Dimensões finais: {largura}x{altura_total} pixels")
    print(f"Salvo como: {output_path}")
    
else:
    print("Nenhuma imagem encontrada para concatenar")

print("Processamento concluído!")