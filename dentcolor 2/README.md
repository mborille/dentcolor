# dentcolor

**Colorimetria para odontologia restauradora: implementação de referência do CIEDE2000 e das conversões CIELAB ↔ sRGB.**

Versão 1.0.0 · Python e JavaScript · Licença MIT

Autor: Marcelo Barboza Borille (CRO-RS 14520)
ORCID: [0009-0000-5422-207X](https://orcid.org/0009-0000-5422-207X)
DOI: [10.6084/m9.figshare.33087674](https://doi.org/10.6084/m9.figshare.33087674)

---

## O que este pacote é, e o que ele não é

Este pacote fornece **método**, não **dados**.

Ele implementa a matemática da diferença de cor e das conversões entre espaços, validada contra referência externa. Ele **não acompanha tabela de coordenadas L\*a\*b\* de nenhuma escala de cor comercial**, e isso é deliberado.

O motivo é simples e vale registrar, porque é a origem deste pacote. Ao construir um simulador de cor para uso clínico, o autor percebeu que as coordenadas L\*a\*b\* que circulavam no próprio material não tinham fonte primária rastreável, e que boa parte do que se encontra publicado na web sobre coordenadas de escalas comerciais tem o mesmo problema. Há ainda uma questão de fundo: medições da mesma escala em espectrofotômetros diferentes divergem em magnitude comparável ao limiar de aceitabilidade clínica. Ou seja, "o L\*a\*b\* do tom X" não é um número, é uma faixa com desvio padrão.

A resposta deste pacote é separar as duas coisas. O código é publicado e verificável. Os dados ficam com quem os mediu, num formato que obriga a declarar procedência.

Se você precisa de coordenadas de escala, meça as suas (veja `schema/`) ou use fonte publicada e cite-a.

---

## Instalação e uso

### Python (3.9 ou superior, sem dependências)

```python
import sys; sys.path.insert(0, "dentcolor")
from dentcolor import ciede2000, lab_to_hex, hex_to_lab, in_srgb_gamut, classify_difference

ciede2000((73.5, 1.5, 14.3), (71.9, 1.8, 17.6))
# 2.2710515179652475

classify_difference(2.271)
# 'inaceitavel'

lab_to_hex((73.5, 1.5, 14.3))
# '#C2B39B'

in_srgb_gamut((50, 120, -120))
# False
```

### JavaScript (módulo ES, navegador ou Node)

```javascript
import { ciede2000, labToHex, inSrgbGamut } from "./dentcolor.js";

ciede2000([73.5, 1.5, 14.3], [71.9, 1.8, 17.6]); // 2.271051517965246
labToHex([73.5, 1.5, 14.3]);                     // '#C2B39B'
```

---

## API

| Função (Python / JS) | O que faz |
|---|---|
| `ciede2000` | Diferença de cor CIEDE2000 (ΔE00), com fatores paramétricos kL, kC, kH |
| `delta_e_cie76` / `deltaECIE76` | Diferença euclidiana CIE76, para comparação histórica |
| `classify_difference` / `classifyDifference` | Classifica um ΔE00 contra os limiares perceptivos |
| `lab_to_xyz` / `labToXyz` | CIELAB para XYZ |
| `xyz_to_lab` / `xyzToLab` | XYZ para CIELAB |
| `lab_to_srgb` / `labToSrgb` | CIELAB para sRGB 8 bits |
| `srgb_to_lab` / `srgbToLab` | sRGB 8 bits para CIELAB |
| `lab_to_hex` / `labToHex` | CIELAB para `#RRGGBB` |
| `hex_to_lab` / `hexToLab` | `#RRGGBB` para CIELAB |
| `in_srgb_gamut` / `inSrgbGamut` | Informa se a cor cabe no sRGB sem recorte |
| `load_shade_table` | Carrega tabela de escala e avisa se a procedência estiver incompleta |
| `nearest_shade` / `nearestShade` | Ordena os tons de uma tabela por ΔE00 em relação a uma cor alvo |

Ponto branco padrão: D65, observador 2 graus (CIE 1931).

---

## Validação

Os números abaixo foram medidos na montagem deste pacote e podem ser reproduzidos rodando `tests/`.

| Verificação | Resultado |
|---|---|
| ΔE00 contra `colour-science` 0.4.7, 200.000 pares aleatórios | discrepância máxima **2,8 × 10⁻¹³** |
| Concordância entre as versões JavaScript e Python, 30.000 pares | discrepância máxima **1,8 × 10⁻¹³** |
| Simetria ΔE(p,q) = ΔE(q,p), 50.000 pares | diferença **exatamente zero** |
| Identidade ΔE(p,p) = 0 | exato |
| Ida e volta CIELAB → XYZ → CIELAB, 10.000 amostras | 9 casas decimais |
| Ida e volta hex → CIELAB → hex, 5.000 cores | exato |
| Casos de borda: croma zero, descontinuidade de matiz em 0/360, extremos de L\* | sem NaN, sem descontinuidade |

A implementação segue a formulação de Sharma, Wu e Dalal (2005), incluindo o tratamento correto da média de matiz e do caso croma zero, que são as duas armadilhas mais comuns em implementações do CIEDE2000.

O conjunto oficial de 34 pares de teste **não é redistribuído** com este pacote. Para verificar conformidade formal, baixe a tabela do material suplementar do artigo original, salve em `tests/sharma2005.csv` com as colunas `L1,a1,b1,L2,a2,b2,dE00` e rode a suíte. Sem esse arquivo, o teste correspondente é pulado e a validação numérica fica por conta da comparação com `colour-science`.

---

## Formato de tabela de escala

`schema/shade-table.schema.json` define como publicar coordenadas de uma escala de modo reprodutível. O bloco `provenance` é obrigatório e tem um campo `status` com quatro valores possíveis:

- `measured` — medido por você. Publique média, desvio padrão e número de leituras.
- `published` — transcrito de fonte citada. Preencha `source_citation` e `source_doi`.
- `provisional` — origem não rastreada. **Não citável.**
- `estimated` — interpolado ou estimado. **Não citável.**

`schema/exemplo-tabela.json` mostra o formato com números inventados, rotulados como tal.

Essa obrigatoriedade é o ponto principal do formato. Uma tabela de escala sem procedência declarada é ilustração, não referência, e a distinção precisa estar no arquivo, não na cabeça de quem o usou.

---

## Limitações que você deve conhecer antes de usar

- **Os limiares perceptivos precisam de conferência.** As constantes `PERCEPTIBILITY_THRESHOLD` (0,8) e `ACCEPTABILITY_THRESHOLD` (1,8) são os valores correntes na literatura odontológica, atribuídos a Paravina e colaboradores (2015). A referência completa **não foi verificada na montagem deste pacote** e está marcada no código como pendente. Confirme no artigo original antes de citar.
- **ΔE00 não é veredito clínico.** A métrica foi ajustada para pares de amostras planas sob condições controladas. Dente é translúcido, tem gradiente de croma no sentido cervico-incisal e opalescência, e nada disso entra na fórmula.
- **Hex é aproximação de tela.** Tons saturados de dentina e alguns tons clareados caem fora do gamut sRGB. Use `in_srgb_gamut` antes de confiar num hex, e prefira ΔE00 sobre inspeção visual em monitor.
- **O pacote não faz gerenciamento de cor.** Não lê perfis ICC, não trata metamerismo, não corrige balanço de branco de fotografia. Entra L\*a\*b\*, sai L\*a\*b\* ou sRGB.

---

## Como citar

Preencha o DOI depois de publicar. Metadados legíveis por máquina em `CITATION.cff`.

```
Borille, M. B. (2026). dentcolor: implementação de referência do CIEDE2000
e conversões CIELAB/sRGB para odontologia restauradora (versão 1.0.0)
[software]. figshare. https://doi.org/10.6084/m9.figshare.33087674
```

---

## Licença

MIT. Veja `LICENSE`.

A escolha é deliberada: licenças Creative Commons não são adequadas para software, e a MIT já obriga a manter o aviso de copyright, que é a atribuição que interessa aqui.

---

## Abstract (EN)

`dentcolor` is a dependency-free reference implementation of the CIEDE2000 colour-difference formula (CIE 142:2001) and CIELAB ↔ sRGB conversions, in Python and JavaScript, aimed at restorative and esthetic dentistry. It ships **method, not data**: no L\*a\*b\* coordinates for any commercial shade guide are bundled. Instead it defines a JSON schema for publishing shade tables in which a provenance block is mandatory and explicitly distinguishes measured, published, provisional and estimated values. The CIEDE2000 implementation agrees with `colour-science` 0.4.7 to within 2.8 × 10⁻¹³ across 200,000 random pairs, and the JavaScript and Python ports agree to within 1.8 × 10⁻¹³. Released under the MIT licence.
