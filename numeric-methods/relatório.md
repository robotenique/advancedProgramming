* João Gabriel Basi             NUSP 9793801
* Juliano Garcia de Oliveira    NUSP 9277086

## EP1 - MAC0210

Criamos uma função *interpolate*, que recebe:

* *x* - Um vetor com as posições na reta x das amostras
* *y* - Um vetor com as respestivas posições na reta y das amostras
* *num_splines* - O número de splines que a função deve utilizar na interpolação
* *lmbda* - O valor do coeficiente de regularização lambda

A função primeiro calcula o valor da matriz *M*, a partir da soma
*m_1* + *lambda* * *m_2*, onde m_1 é 
