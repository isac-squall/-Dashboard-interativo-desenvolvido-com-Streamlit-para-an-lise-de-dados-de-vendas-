#!/bin/bash
# Script para inicializar o repositório Git

echo "=========================================="
echo "📦 Inicializando repositório Git"
echo "=========================================="

# Inicializar Git
git init

# Adicionar branches
git branch -M main

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "chore: projeto inicial com estrutura completa

- Dashboard Streamlit funcional
- Configuração de ambiente virtual
- Documentação completa
- Estrutura de projeto profissional"

echo ""
echo "=========================================="
echo "✅ Repositório Git inicializado!"
echo "=========================================="
echo ""
echo "Próximas etapas:"
echo "1. Adicione o remote: git remote add origin <url-do-repositorio>"
echo "2. Push para o repositório: git push -u origin main"
echo ""
