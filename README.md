# Projeto
Projeto desenvolvido ao longo da disciplina Visão Natural e Artificial 
oferecida pelo programa de Pós-Graduação do Instituto de Física de São Carlos.

## Como Funciona?

A objetivo deste programa é reconhecer as bordas dos objetos presentes nas 
imagens fornecidas. Para tanto, foram escolhidas imagens 256x256 em escala de cinza, 
as quais estão presentes no arquivo imagens.tar.gz. Para descompactar este arquivo, 
basta o comando:

```bash
tar -xzf imagens.tar.gz
```

Em seguida, o programa pode ser executado pelo comando:

```bash
python script.py
```

Após a execução do programa, alguns diretórios serão criados no diretório onde o 
programa se enconta. Cada um deles representa o resultado obtido ao se submeter as 
imagens por processamentos intermediários antes que possamos finalmente obter as bordas. 
Vamos à cada um deles e um pouco sobre a teoria envolvida em cada etapa.

### dog\_images 

Este diretório armazena os resultado obtido após uma imagem passar pelo procedimento 
[DoG](https://en.wikipedia.org/wiki/Difference_of_Gaussians), o qual, em suma, consiste em 
realizar uma [convolução](https://en.wikipedia.org/wiki/Convolution) da imagem com uma gaussiana.

Porém, convoluções são difíceis de fazer. Isso nos obriga trocarmos de espaço, em busca de um onde 
a convolução possa ser substituída por uma operação mais simples. E este espaço existe de fato e é 
obtido através da [Transformada de Fourier](https://en.wikipedia.org/wiki/Fourier_transform) da imagem.

Após aplicarmos uma [Transformada Rápida de Fourier](https://en.wikipedia.org/wiki/Fast_Fourier_transform) 
sobre a imagem (a gaussiana também deveria passar por este processo, porém a transformada de uma gaussiana é 
uma gaussiana, logo podemos criar as nossas já neste espaço, sem se precoupar em realizar a sua transformada) 
podemos apenas, ao invés da convolução, realizar uma simples multiplicação entre as duas funções.

Neste ponto, devemos ter cuidado de não cair na tentação de multiplicarmos as funções sem antes realizarmos 
um deslocamento da gaussiana para que seu referencial esteja de acordo com o da imagem. Após isso, a multiplicação 
pode ser feita sem problemas!

Após isso, basta fazermos a [Transformada Inversa de Fourier](https://en.wikipedia.org/wiki/Fourier_inversion_theorem) 
e plotar o resultado final.
