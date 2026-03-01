# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - 2026-03-01

### Added
- ✅ Dashboard interativo com Streamlit
- ✅ Suporte para upload de CSV, XLS e XLSX
- ✅ 3 abas de análise: Vendas, Clientes, Produtos
- ✅ Cálculos automáticos de KPIs
  - Receita Total
  - Número de Ordens
  - Ticket Médio
  - Taxa de Conversão
  - CAC (Customer Acquisition Cost)
  - Crescimento Mensal
- ✅ Gráficos interativos com Plotly
- ✅ Filtros dinâmicos (filial, categoria, cliente, gênero)
- ✅ Exportação para CSV e Excel
- ✅ Cálculos de Margem e Lucro
- ✅ Suporte a múltiplas moedas e formatações

### Changed
- 🔧 Refatoração completa do código base
- 🔧 Melhor tratamento de exceções
- 🔧 Logging estruturado

### Fixed
- 🐛 Correção no formato da coluna de mês (YYYY-MM)
- 🐛 Erro ao carregar arquivo padrão (caminho relativo)
- 🐛 Type hints e docstrings

### Security
- 🔒 Validação de entrada de dados
- 🔒 Tratamento seguro de exceções

---

## Versões Anteriores

### [0.1.0] - 2026-02-28 (Beta)
- Versão inicial com funcionalidades básicas
- Prototipagem de conceito
