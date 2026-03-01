# Exemplo de estrutura de dados esperada
# Este arquivo documenta o formato esperado do CSV

## Colunas Obrigatórias:
- **Data/Date**: Coluna com a data da transação (formatos aceitos: YYYY-MM-DD, DD/MM/YYYY, etc)

## Colunas Numéricas (valores):
- **Sale Amount / Valor de Venda**: Valor da transação (decimal, separado por vírgula)
- **Cost / Custo**: Custo da venda (opcional)
- **Margin / Margem**: Margem percentual (opcional)
- **Rating / Avaliação**: Avaliação ou nota (opcional)

## Colunas de Categoria (texto):
- **City / Cidade / Filial / Branch**: Localização ou unidade
- **Product Category / Categoria / Product Line**: Tipo ou categoria de produto
- **Customer Type / Tipo de Cliente**: Pessoa física, jurídica, etc
- **Gender / Sexo / Gênero**: M, F, etc (opcional)
- **Payment Method / Forma de Pagamento**: Cartão, Dinheiro, PIX, etc (opcional)

## Formato do CSV:
```
Data;Cidade;Categoria;Tipo de Cliente;Gênero;Forma de Pagamento;Valor;Custo;Avaliação
01/01/2024;São Paulo;Eletrônicos;Pessoa Física;M;Cartão;250,00;100,00;4.5
02/01/2024;Rio de Janeiro;Alimentos;Pessoa Jurídica;F;Dinheiro;150,50;50,00;4.0
```

## Encoding:
- **Encoding**: UTF-8
- **Separador**: ; (ponto-e-vírgula)
- **Decimal**: , (vírgula)

## Dicas:
1. Certifique-se que todas as datas estão no mesmo formato
2. Use valores numéricos sem símbolos de moeda ($, R$, etc)
3. Nomes de colunas sem espaços no início/final
4. Remova linhas completamente vazias
5. Verifique se há caracteres especiais problemáticos

## Tamanho máximo:
- Streamlit recomenda máx. 200MB de dados
- Para melhor performance, use <= 50MB
