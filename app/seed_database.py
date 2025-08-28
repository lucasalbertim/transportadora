#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.utils.seed_data import seed_all_data


def main():
    """Função principal para executar o seed"""
    db = SessionLocal()
    try:
        seed_all_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()