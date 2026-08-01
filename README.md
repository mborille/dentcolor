# dentcolor

Implementação em código aberto de conversão **CIELAB ↔ sRGB** e cálculo de diferença de cor **CIEDE2000 (ΔE00)**, escrita para uso em odontologia restauradora e estética.

Disponível em duas versões numericamente equivalentes: **Python** (`dentcolor.py`) e **JavaScript** (`dentcolor.js`).

O pacote alimenta o simulador de cor disponível em
<https://www.lentedecontatodental.poa.br/simulador-de-cor/>

---

## Escopo

Esta biblioteca fornece **método, não dados.**

Ela implementa as transformações colorimétricas e a fórmula de diferença de cor. Ela **não** acompanha tabela de coordenadas L\*a\*b\* de nenhuma escala de cor comercial. Quem for usar precisa fornecer as próprias coordenadas, medidas em espectrofotômetro ou obtidas de fonte que possa citar.

Essa separação é deliberada. Coordenadas de escalas comerciais variam conforme lote, instrumento, geometria de medição e condição de iluminação. Embutir uma tabela fixa daria ao usuário uma precisão que ela não tem.

### Como fornecer sua tabela

O formato esperado está descrito em [`shade-table.schema.json`](shade-table.schema.json), com um exemplo preenchido em [`exemplo-tabela.json`](exemplo-tabela.json).

O schema define a estrutura; os valores são seus. Documente a procedência das coordenadas que você usar, seja medição própria em espectrofotômetro ou fonte publicada que possa citar.

## O que faz

- Conversão entre coordenadas CIELAB e sRGB
- Cálculo de ΔE00 pela fórmula CIEDE2000 (CIE 142:2001)
- Ponto branco D65, observador padrão 2°

A versão JavaScript é porte da implementação de referência em Python, com concordância verificada abaixo de 1e-9 em ΔE00. Os testes que verificam essa equivalência estão em [`test_dentcolor.py`](test_dentcolor.py).

## O que não faz

Não substitui espectrofotometria. As cores exibidas em tela dependem de calibração do monitor, do perfil de cor do sistema e das condições de iluminação do ambiente. Qualquer decisão clínica de cor deve ser tomada com instrumento adequado e sob condições controladas.

---

## Limiares de perceptibilidade e aceitabilidade

O pacote expõe duas constantes de referência:

| Constante | Valor (ΔE00) | Significado |
|---|---|---|
| `PERCEPTIBILITY_THRESHOLD` | 0,8 | Limiar 50:50% de perceptibilidade |
| `ACCEPTABILITY_THRESHOLD` | 1,8 | Limiar 50:50% de aceitabilidade |

Esses valores **não são arbitrários nem próprios deste pacote**. Provêm de:

> Paravina RD, Ghinea R, Herrera LJ, Bona AD, Igiel C, Linninger M, Sakai M, Takahashi H, Tashkandi E, Perez MdelM.
> **Color difference thresholds in dentistry.**
> *Journal of Esthetic and Restorative Dentistry*. 2015;27 Suppl 1:S1-9.
> DOI: [10.1111/jerd.12149](https://doi.org/10.1111/jerd.12149) · PMID: 25886208

Estudo multicêntrico prospectivo com 175 observadores em sete centros, que reporta os limiares 50:50% de perceptibilidade e aceitabilidade para cerâmica odontológica em CIELAB e em CIEDE2000.

**Ressalva de uso.** Os limiares foram determinados para cerâmica monocromática em cabine de visualização, sob condição controlada. Eles servem como referência de controle de qualidade, não como critério clínico automático. O próprio estudo relata diferença estatisticamente significativa entre grupos de observadores: dentistas, técnicos, auxiliares e leigos não julgam igual. Aplicar um número único a toda situação clínica ignora essa variabilidade.

---

## Como citar

A versão arquivada e citável deste pacote está depositada no Figshare, com DOI permanente:

> Borille, MB. **dentcolor**: implementação CIELAB/sRGB e CIEDE2000 para odontologia estética. Figshare, 2026.
> DOI: [10.6084/m9.figshare.33087674](https://doi.org/10.6084/m9.figshare.33087674)

Prefira citar o DOI, não a URL deste repositório. Repositórios podem ser renomeados ou movidos; o DOI não.

O botão **Cite this repository**, no topo desta página, gera a citação formatada a partir do arquivo `CITATION.cff`.

---

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).

Você pode usar, modificar e redistribuir, inclusive comercialmente, mantendo o aviso de copyright e a ressalva de garantia.

## Contribuições

Correções são bem-vindas por *issue* ou *pull request*. Para correções de valores de referência ou de citação, indique a fonte primária.

---

## Autor

**Marcelo Barboza Borille** · Cirurgião-Dentista, CRO-RS 14520
ORCID: [0009-0000-5422-207X](https://orcid.org/0009-0000-5422-207X)

---

## English summary

Open-source implementation of **CIELAB ↔ sRGB** conversion and **CIEDE2000 (ΔE00)** colour difference, written for restorative and esthetic dentistry. Available in equivalent Python and JavaScript versions, with equivalence tests in [`test_dentcolor.py`](test_dentcolor.py).

**Scope: this library provides method, not data.** It ships no L\*a\*b\* coordinate table for any commercial shade guide. Users must supply their own coordinates, measured with a spectrophotometer or drawn from a citable source. The expected format is defined in [`shade-table.schema.json`](shade-table.schema.json), with a worked example in [`exemplo-tabela.json`](exemplo-tabela.json).

The two exported thresholds (ΔE00 0.8 for perceptibility, 1.8 for acceptability) come from Paravina RD et al., *Color difference thresholds in dentistry*, J Esthet Restor Dent 2015;27 Suppl 1:S1-9, [DOI 10.1111/jerd.12149](https://doi.org/10.1111/jerd.12149). They were determined for monochromatic dental ceramic under controlled viewing conditions and serve as quality-control references, not as automatic clinical criteria.

Archived, citable version: DOI [10.6084/m9.figshare.33087674](https://doi.org/10.6084/m9.figshare.33087674). MIT licensed.
