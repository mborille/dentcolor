# Metadados para o depósito no Figshare

Copie campo a campo. O que estiver entre colchetes precisa da sua decisão.

---

## Item type

**Software**

Não use "Figure" nem "Dataset". Software é o tipo correto e é o que faz o
Figshare gerar os metadados de citação certos.

---

## Title

```
dentcolor: implementação de referência do CIEDE2000 e conversões CIELAB/sRGB para odontologia restauradora
```

---

## Description

```
dentcolor é uma implementação de referência, sem dependências, da fórmula de
diferença de cor CIEDE2000 (CIE 142:2001) e das conversões CIELAB/sRGB, em
Python e JavaScript, voltada à odontologia restauradora e estética.

O pacote fornece método, não dados. Nenhuma coordenada L*a*b* de escala de cor
comercial acompanha o software. Essa ausência é deliberada: coordenadas de
escalas que circulam livremente costumam ter fonte primária não rastreável, e
medições da mesma escala em espectrofotômetros diferentes divergem em magnitude
comparável ao limiar de aceitabilidade clínica. Em vez de embutir números de
procedência incerta, o pacote define um esquema JSON para publicação de tabelas
de escala no qual o bloco de procedência é obrigatório e distingue
explicitamente valores medidos, publicados, provisórios e estimados.

Validação: a implementação do CIEDE2000 concorda com a biblioteca
colour-science 0.4.7 dentro de 2,8 x 10^-13 em 200.000 pares aleatórios; as
versões JavaScript e Python concordam entre si dentro de 1,8 x 10^-13; a
simetria da métrica é exata; e os casos de borda conhecidos (croma zero,
descontinuidade de matiz em 0/360 graus, extremos de luminosidade) são tratados
sem descontinuidade. A suíte de testes acompanha o pacote e reproduz esses
números.

Conteúdo: biblioteca em Python e em JavaScript, esquema JSON para tabelas de
escala com exemplo, suíte de testes, e documentação com as limitações
explicitadas.

Licença: MIT.

---

[EN] dentcolor is a dependency-free reference implementation of the CIEDE2000
colour-difference formula (CIE 142:2001) and CIELAB/sRGB conversions, in Python
and JavaScript, aimed at restorative and esthetic dentistry. It ships method,
not data: no L*a*b* coordinates for any commercial shade guide are bundled.
Instead it defines a JSON schema for publishing shade tables in which a
provenance block is mandatory and explicitly distinguishes measured, published,
provisional and estimated values. The CIEDE2000 implementation agrees with
colour-science 0.4.7 to within 2.8e-13 across 200,000 random pairs, and the
JavaScript and Python ports agree to within 1.8e-13. Released under the MIT
licence.
```

---

## Categories

Busque e marque, nesta ordem de prioridade:

1. `Dentistry` (ou a subcategoria de materiais dentários, se aparecer)
2. `Colour science` ou `Optics`, se o seletor oferecer
3. `Software engineering`, se houver

Não deixe vazio. Foi o erro que aconteceu com o subject do componente no OSF.

---

## Keywords

```
CIEDE2000
CIELAB
diferença de cor
color difference
seleção de cor
shade matching
odontologia estética
esthetic dentistry
colorimetria
dental colorimetry
sRGB
lente de contato dental
laminado cerâmico
open source
```

---

## License

**MIT**

Se o seletor do Figshare não oferecer MIT para o tipo Software, escolha a
opção de licença de software mais próxima e mantenha o arquivo `LICENSE` no
pacote, que é o que vale juridicamente. Não escolha CC-BY aqui: Creative
Commons não é adequada para software, e a MIT já obriga a manter o aviso de
copyright, que é a atribuição que interessa.

---

## Funding

Deixe em branco, salvo se houver financiamento a declarar.

---

## References / Related materials

Adicione os DOIs que você já tem, para o Figshare ligar os itens do seu perfil:

```
https://doi.org/10.17605/OSF.IO/AG62Q
https://doi.org/10.17605/OSF.IO/XF26U
https://doi.org/10.17605/OSF.IO/Z5WHK
```

---

## Depois de publicar

1. Confira que o DOI publicado é o mesmo que foi reservado: 10.6084/m9.figshare.33087674
2. O DOI já está gravado no pacote (README, CITATION.cff, o `$id` do schema e
   o cabeçalho dos dois módulos), porque foi reservado antes da publicação.
   Nada a substituir depois.
3. Adicione ao ORCID por DOI, tipo "software".
4. Confirme que o seu iD do ORCID aparece no registro do item publicado.
5. Cite o DOI na página do simulador no site.

---

## Uma nota sobre a sequência

Este depósito é o primeiro de dois. O segundo é a tabela de escala medida por
você, publicada no formato definido por `schema/shade-table.schema.json`, com
média, desvio padrão e número de leituras por tab. O segundo cita o primeiro.

Essa é a razão pela qual vale publicar o método antes do dado: quando a
medição sair, ela chega num formato que já existe, já tem DOI e já foi
declarado publicamente. É assim que um perfil acadêmico deixa de ser uma
coleção de itens soltos e passa a parecer um programa de pesquisa.
