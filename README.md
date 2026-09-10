# Radar APS

Ferramenta pública de análise territorial para gestores da Atenção Primária à Saúde.

## Objetivo

O Radar APS organiza dados públicos oficiais para apoiar a priorização de territórios e a leitura de desigualdades em saúde. O primeiro MVP combina município, Região de Saúde, CNES/UBS e população do IBGE. O indicador de Internações por Condições Sensíveis à Atenção Primária (ICSAP) só será publicado quando a origem e a derivação oficial forem validadas.

## Princípios

- dados agregados; nunca prontuários ou identificadores pessoais;
- fonte, período, transformação e limitações documentados;
- observado, estimado e indisponível nunca são misturados;
- scripts reproduzíveis antes de telas bonitas;
- ausência de dado é exibida, não preenchida com invenção;
- atualização local e barata, com publicação de artefatos auditáveis.

## Estrutura

- `scripts/` — ingestão determinística;
- `data/raw/` — downloads locais, ignorados pelo Git;
- `data/processed/` — artefatos derivados, ignorados por padrão;
- `docs/` — contrato de dados e decisões metodológicas;
- `site/` — painel estático inicial;
- `LICENSE` — Apache-2.0 para código;
- `LICENSE-DOCS` — CC BY 4.0 para documentação.

## Execução local

```bash
python3 scripts/ingest_metadata.py --output data/raw
python3 -m http.server 8080 --directory site
```

O ingest usa as APIs públicas oficiais do Ministério da Saúde e do IBGE. Não exige token.

## Estado do MVP

- [x] nome, escopo e política de fontes definidos;
- [x] contrato inicial de dados documentado;
- [x] ingestão de regiões de saúde, UBS/CNES e municípios/IBGE;
- [ ] validar fonte oficial do SIH para derivar ICSAP;
- [ ] fechar fórmula e denominador do ranking;
- [ ] completar ranking, mapa e série histórica;
- [ ] publicar repositório público após autenticação GitHub e revisão final.

## Licenças e fontes

O código está sob Apache-2.0 e a documentação sob CC BY 4.0. Dados baixados ou derivados permanecem sujeitos aos termos e atribuições das fontes DATASUS/Ministério da Saúde e IBGE. Consulte `docs/DATA_CONTRACT.md`.
