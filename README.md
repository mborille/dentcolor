# dentcolor

Implementação em código aberto de conversão **CIELAB ↔ sRGB** e cálculo de diferença de cor **CIEDE2000 (ΔE00)**, escrita para uso em odontologia estética.

O pacote alimenta o simulador de cor disponível em
<https://www.lentedecontatodental.poa.br/simulador-de-cor/>

---

## O que faz

- Conversão entre coordenadas CIELAB e sRGB
- Cálculo de ΔE00 pela fórmula CIEDE2000
- Rotinas de apoio para representação visual de escalas de cor dental

## O que não faz

Não substitui espectrofotometria. As cores exibidas em tela dependem de calibração do monitor, do perfil de cor do sistema e das condições de iluminação do ambiente. Qualquer decisão clínica de cor deve ser tomada com instrumento adequado e sob condições controladas.

---

## Procedência das coordenadas da escala VITA

> **Leia antes de reutilizar.** As coordenadas L\*a\*b\* da escala VITA embutidas neste código foram obtidas por levantamento em fontes secundárias e **não foram verificadas pelo autor contra documentação técnica primária do fabricante nem contra medição própria em espectrofotômetro**.
>
> Elas servem para demonstração e ensino. Se você pretende usar este código para pesquisa, para comparação de materiais ou para qualquer finalidade em que a exatidão colorimétrica importe, verifique os valores contra a documentação oficial da VITA Zahnfabrik ou meça diretamente as escalas antes de confiar nos resultados.
>
> Correções são bem-vindas por *issue* ou *pull request*, preferencialmente com indicação da fonte primária.

Essa ressalva está aqui de propósito. Um simulador de cor que não declara a origem dos seus valores de referência convida a erros que não aparecem na tela.

---

## Como citar

A versão arquivada e citável deste pacote está depositada no Figshare, com DOI permanente:

> Borille, M. **dentcolor**: implementação CIELAB/sRGB e CIEDE2000 para odontologia estética. Figshare, 2026.
> DOI: [10.6084/m9.figshare.33087674](https://doi.org/10.6084/m9.figshare.33087674)

Prefira citar o DOI, não a URL deste repositório. Repositórios podem ser renomeados ou movidos; o DOI não.

---

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).

Você pode usar, modificar e redistribuir, inclusive comercialmente, mantendo o aviso de copyright e a ressalva de garantia.

---

## Autor

**Marcelo Barboza Borille** · Cirurgião-Dentista, CRO-RS 14520
ORCID: [0009-0000-5422-207X](https://orcid.org/0009-0000-5422-207X)

---

## English summary

Open-source implementation of **CIELAB ↔ sRGB** conversion and **CIEDE2000 (ΔE00)** colour difference, written for use in esthetic dentistry. Powers the colour simulator at the URL above.

**Important:** the VITA shade guide L\*a\*b\* coordinates embedded in this code were compiled from secondary sources and have **not** been verified by the author against the manufacturer's primary technical documentation or against own spectrophotometric measurement. They are adequate for demonstration and teaching. Verify them before using this code where colourimetric accuracy matters.

Archived, citable version: DOI [10.6084/m9.figshare.33087674](https://doi.org/10.6084/m9.figshare.33087674). MIT licensed.
