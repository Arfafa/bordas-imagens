# Projeto
Projeto desenvolvido ao longo da disciplina Visão Natural e Artificial 
oferecida pelo programa de Pós-Graduação do Instituto de Física de São Carlos.

## Como Funciona?

O objetivo deste programa é reconhecer as bordas dos objetos presentes nas 
imagens fornecidas. Para tanto, foram escolhidas imagens 256x256 em escala de cinza, 
as quais estão presentes no arquivo imagens.tar.gz. Para descompactar este arquivo, 
basta o comando:

```bash
$ tar -xzf imagens.tar.gz
```

Em seguida, o programa pode ser executado pelo comando:

```bash
$ python script.py
```

Após a execução do programa, alguns diretórios serão criados no diretório onde o 
programa se enconta. Cada um deles representa o resultado obtido ao se submeter as 
imagens por processamentos intermediários antes que possamos finalmente obter as bordas. 
Vamos à cada um deles e um pouco sobre a teoria envolvida em cada etapa.

### dog\_images 

Este diretório armazena o resultado obtido após uma imagem passar pelo procedimento 
[DoG](https://en.wikipedia.org/wiki/Difference_of_Gaussians), o qual, em suma, consiste em 
realizar uma [convolução](https://en.wikipedia.org/wiki/Convolution) da imagem com uma gaussiana.

Porém, convoluções são difíceis de fazer. Isso nos obriga trocarmos de espaço, em busca de um onde 
a convolução possa ser substituída por uma operação mais simples. E este espaço existe de fato e é 
obtido através da [Transformada de Fourier](https://en.wikipedia.org/wiki/Fourier_transform) da imagem.

Após aplicarmos uma [Transformada Rápida de Fourier](https://en.wikipedia.org/wiki/Fast_Fourier_transform) 
sobre a imagem (a gaussiana também deveria passar por este processo, porém a transformada de uma gaussiana é 
uma gaussiana, logo podemos criar as nossas já neste espaço, sem se precoupar em realizar a sua transformada) 
podemos apenas, ao invés da convolução, realizar uma simples multiplicação entre as duas funções.

Neste ponto, devemos ter cuidado de não cair na tentação de multiplicarmos as funções sem antes realizarmos um 
[deslocamento da gaussiana](https://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.ifftshift.html#numpy.fft.ifftshift) 
para que seu referencial esteja de acordo com o da imagem. Após isso, a multiplicação pode ser feita sem problemas!

Após isso, basta fazermos a [Transformada Inversa de Fourier](https://en.wikipedia.org/wiki/Fourier_inversion_theorem) 
e plotar o resultado.

### log\_images

Este diretório armazena o resultado obtido após uma imagem passar pelo procedimento 
[LoG](https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm), o qual dá um passo além em relação ao processo DoG 
citado anteriormente. O LoG consiste em aplicar o [Operador Laplaciano](https://en.wikipedia.org/wiki/Laplace_operator) 
sobre o resultado do DoG.

Porém, uma forma mais simples de aplicar este operador é no mesmo espaço encontrado através da Transformada de Fourier. 
Neste espaço, a [derivada de segunda ordem](https://en.wikipedia.org/wiki/Second_derivative) presente no Laplaciano 
dá lugar a uma operação mais simples dada por:

![equation](https://latex.codecogs.com/gif.latex?L&space;=&space;-(x^2&space;&plus;&space;y^2))

Enretanto, antes de realizar a multiplicação do DoG com a equação acima, esta deve passar pelo mesmo processo 
de deslocamento para alinhar o referencial do Laplaciano com o da imagem. Após isso, a multiplicação pode ser 
realizada sem grandes problemas (assim como Transformada Inversa de Fourier) e o resultado pode ser plotado.

### lim\_images

Este diretório armazena o resultado obtido após uma imagem passar pelo procedimento de 
[limiarização](https://en.wikipedia.org/wiki/Thresholding_(image_processing)).

Este processo consiste em fazer com que os pixels com valores maiores que zero tenham seu valor alterado para 
1 (branco), e, caso contrário, o valor é modificado para zero (preto). Após esta binarização da imagem o resultado 
é plotado.

### borders

Este diretório armazena o resultado obtido após uma imagem passar por um procedimento que busca ressaltar 
as bordas dos objetos presentes na mesma. Para isso, é utilizado um processo conhecido como 
[Vizinhança-4](http://www.facom.ufu.br/~backes/gsi058/Aula03-Conectividade.pdf) que consiste em analisar 
os pixels brancosr. Caso o pixel em questão possua algum vizinho preto ele está na borda e permanece branco, 
do contrário, ele se encontra no interior do objeto e seu valor é trocado para zero (preto).
