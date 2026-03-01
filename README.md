# Dashboard de Vendas - Supermercado

Dashboard interativo desenvolvido com Streamlit para análise de dados de vendas de supermercado.

## 📋 Requisitos

- Python 3.10+
- pip ou uv

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd Dash.pyton
```

### 2. Criar ambiente virtual
```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

## 📊 Como usar

Execute o dashboard com:
```bash
streamlit run "Supermarket Sales/dashboards.py"
```

O navegador abrirá automaticamente em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
Dash.pyton/
├── Supermarket Sales/
│   ├── dashboards.py          # Aplicação principal
│   └── supermarket_sales.csv   # Dados padrão
├── requirements.txt            # Dependências Python
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## ✨ Funcionalidades

- **Upload de arquivos**: Suporte para CSV, XLS e XLSX
- **Análise mensal**: Filtros por mês, filial, categoria e tipo de cliente
- **KPIs**: Receita, ordens, ticket médio, taxa de conversão, CAC
- **Visualizações**: Gráficos interativos com Plotly
- **3 Abas de análise**:
  - Vendas: Tendências e desempenho
  - Clientes: Segmentação e comportamento
  - Produtos: Performance por categoria

## 🔧 Características Técnicas

- Type hints para melhor legibilidade
- Tratamento robusto de exceções
- Logging estruturado
- Validação de dados
- Cálculos automáticos de métricas
- Exportação para CSV e Excel

## 📝 Notas

- Os dados padrão devem estar no mesmo diretório que `dashboards.py`
- O CSV deve usar `;` como separador e `,` como decimal (formato BR)
- Requer colunas de data para funcionalidade completa

## 📧 Suporte

Para problemas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ em 2026**
