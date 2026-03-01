#!/usr/bin/env python3
"""
Script de setup para o Dashboard de Vendas.
Execute: python setup_env.py
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Função principal de setup."""
    print("=" * 60)
    print("🛒 Dashboard de Vendas - Setup Inicial")
    print("=" * 60)
    
    # Detectar sistema operacional
    is_windows = sys.platform.startswith("win")
    
    # Caminho do projeto
    project_root = Path(__file__).parent
    
    # 1. Criar ambiente virtual
    print("\n1️⃣ Criando ambiente virtual...")
    venv_path = project_root / ".venv"
    
    if venv_path.exists():
        print("✅ Ambiente virtual já existe")
    else:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            check=True
        )
        print("✅ Ambiente virtual criado")
    
    # 2. Determinar comando de ativação
    if is_windows:
        activate_cmd = venv_path / "Scripts" / "activate.bat"
        pip_cmd = venv_path / "Scripts" / "pip.exe"
    else:
        activate_cmd = venv_path / "bin" / "activate"
        pip_cmd = venv_path / "bin" / "pip"
    
    # 3. Instalar dependências
    print("\n2️⃣ Instalando dependências...")
    requirements_file = project_root / "requirements.txt"
    
    if requirements_file.exists():
        result = subprocess.run(
            [str(pip_cmd), "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
        else:
            print("❌ Erro ao instalar dependências:")
            print(result.stderr)
            return False
    else:
        print("⚠️  Arquivo requirements.txt não encontrado")
        return False
    
    # 4. Mensagem final
    print("\n" + "=" * 60)
    print("✅ Setup concluído com sucesso!")
    print("=" * 60)
    
    print("\n📋 Próximos passos:")
    if is_windows:
        print(f"1. Ative o ambiente: .\\venv\\Scripts\\Activate.ps1")
    else:
        print(f"1. Ative o ambiente: source {venv_path}/bin/activate")
    
    print("2. Execute o dashboard: streamlit run \"Supermarket Sales/dashboards.py\"")
    print("\n🌐 O browser abrirá em: http://localhost:8501")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
