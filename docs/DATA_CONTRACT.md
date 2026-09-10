# Contrato inicial de dados

## Fontes oficiais

| Domínio | Fonte | Uso | Estado |
|---|---|---|---|
| Regiões de Saúde | API Dados Abertos do Ministério da Saúde | município, região e macrorregião | validado |
| CNES/UBS | API Dados Abertos do Ministério da Saúde | estabelecimentos e UBS | validado |
| População/municípios | API de localidades do IBGE | denominadores territoriais e nomes oficiais | validado |
| ICSAP | SIH/SUS ou indicador oficial equivalente | internações sensíveis à APS | pendente de validação |

## Chaves

- `codigo_municipio`: chave territorial oficial para cruzamentos municipais;
- `codigo_cnes`: chave do estabelecimento de saúde;
- `codigo_regiao_saude`: chave regional do Ministério da Saúde;
- identificadores pessoais não fazem parte do contrato.

## Regras de qualidade

1. Cada registro deve preservar fonte, URL, data de coleta e período de referência.
2. Códigos territoriais não devem ser convertidos em nomes como substituição da chave.
3. Cruzamentos sem correspondência devem ser contabilizados e publicados como falha de cobertura.
4. Uma internação não será atribuída a uma UBS sem vínculo metodologicamente defensável.
5. Taxas só serão calculadas quando o denominador e a população de referência estiverem documentados.
6. O dashboard deve distinguir `observado`, `estimado`, `indisponível` e `não aplicável`.

## ICSAP

A API aberta consultada do Ministério da Saúde não apresentou um endpoint direto de ICSAP/SIH no catálogo atual. O Radar APS não deve criar um índice substituto e chamá-lo de ICSAP. A derivação será implementada somente após:

- identificar o arquivo oficial do SIH ou indicador oficial já calculado;
- conferir dicionário e período;
- documentar a classificação de condições sensíveis;
- validar agregação territorial e denominador;
- criar testes com totais de controle.
