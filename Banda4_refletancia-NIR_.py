import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.enums import Resampling

def carregar_banda_redimensionada(caminho_banda, escala=0.5):
    with rasterio.open(caminho_banda) as banda:
        nova_altura = int(banda.height * escala)
        nova_largura = int(banda.width * escala)

        array = banda.read(
            1,
            out_shape=(nova_altura, nova_largura),
            resampling=Resampling.bilinear
        ).astype(np.float32)

        return array

def calcular_diferenca_refletancia(banda_antes, banda_depois):
    min_linhas = min(banda_antes.shape[0], banda_depois.shape[0])
    min_colunas = min(banda_antes.shape[1], banda_depois.shape[1])

    banda_antes_corte = banda_antes[:min_linhas, :min_colunas]
    banda_depois_corte = banda_depois[:min_linhas, :min_colunas]

    return banda_antes_corte - banda_depois_corte

caminho_banda_antes = 'antes.tif'
caminho_banda_depois = 'depois.tif'

# Reduz resolução pela metade
banda_antes = carregar_banda_redimensionada(caminho_banda_antes)
banda_depois = carregar_banda_redimensionada(caminho_banda_depois)

diferenca_refletancia = calcular_diferenca_refletancia(banda_antes, banda_depois)

plt.figure(figsize=(10, 8))
plt.imshow(diferenca_refletancia, cmap='coolwarm', rasterized=True,
           vmin=-np.nanmax(abs(diferenca_refletancia)), vmax=np.nanmax(abs(diferenca_refletancia)))
plt.colorbar(label='Diferença de refletância')
plt.title('Diferença na Refletância da Banda 4 (NIR)')
plt.axis('off')
plt.tight_layout()
plt.show()
