* João Gabriel Basi             NUSP 9793801
* Juliano Garcia de Oliveira    NUSP 9277086

## EP1 - MAC0210

Criamos uma função *interpolate*, que recebe:

* *x* - Um vetor com as posições na reta x das amostras
* *y* - Um vetor com as respectivas posições na reta y das amostras
* *num_splines* - O número de splines que a função deve utilizar na interpolação
* *lmbda* - O valor do coeficiente de regularização lambda

A função primeiro calcula o valor da matriz *mu*, que é o valor de cada spline,
com peso 1, em cada ponto do vetor *x*. Após isso a função calcula o valor da
matriz *m_1* como sendo *mu* transposta multiplicada por *mu*, calcula também
o valor de *b* como sendo *mu* transposta multiplicada por *y* transposta e
calcula *m_2* utilizando a função *matrix_m2* já fornecida. Por fim ela calcula
o valor de *M* como sendo a soma de *m_1* + *lambda* * *m_2* e retorna os pesos
finais, *res*, como sendo a solução de *M* * *res* = *b*.
