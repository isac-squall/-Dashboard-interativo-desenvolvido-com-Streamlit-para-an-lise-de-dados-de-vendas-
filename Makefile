.PHONY: help install dev test lint format clean run setup

help:
	@echo "Dashboard de Vendas - Available Commands"
	@echo "========================================="
	@echo "make install    - Instalar dependências"
	@echo "make dev        - Instalar dependências de desenvolvimento"
	@echo "make run        - Executar o dashboard"
	@echo "make lint       - Verificar código (flake8)"
	@echo "make format     - Formatar código (black)"
	@echo "make test       - Executar testes (pytest)"
	@echo "make clean      - Limpar arquivos temporários"
	@echo "make setup      - Setup completo do projeto"
	@echo ""

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install black flake8 mypy pytest pytest-cov

run:
	streamlit run "Supermarket Sales/dashboards.py"

lint:
	flake8 "Supermarket Sales/" --max-line-length=100

format:
	black "Supermarket Sales/" --line-length=100

test:
	pytest tests/ -v --cov

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

setup:
	python setup_env.py
	$(MAKE) dev

venv:
	python -m venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate with: source .venv/bin/activate (Linux/Mac) or .venv\Scripts\Activate.ps1 (Windows)"

git-setup:
	@echo "Initializing Git repository..."
	git init
	git add .
	git commit -m "chore: initial commit with project structure"
	@echo "✅ Git repository initialized!"
	@echo "Add remote with: git remote add origin <your-repo-url>"
	@echo "Push with: git push -u origin main"

freeze:
	pip freeze > requirements.txt
	@echo "✅ requirements.txt updated"
