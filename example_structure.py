#!/usr/bin/env python3

import os
import json

def print_project_structure():
    """Print the structure of the project."""
    print("=" * 50)
    print("Проект Telegram бота для отслеживания питания успешно создан!")
    print("=" * 50)
    
    # Get all files in the project
    all_files = []
    for root, dirs, files in os.walk('.'):
        # Skip venv and git directories
        if 'venv' in root or '.git' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                all_files.append(os.path.join(root, file))
    
    # Group files by module
    modules = {
        'config': [],
        'core': [],
        'dto': [],
        'scenarios': [],
        'services': [],
        'tests': [],
        'root': []
    }
    
    for file_path in all_files:
        if '/config/' in file_path:
            modules['config'].append(file_path)
        elif '/core/' in file_path:
            modules['core'].append(file_path)
        elif '/dto/' in file_path:
            modules['dto'].append(file_path)
        elif '/scenarios/' in file_path:
            modules['scenarios'].append(file_path)
        elif '/services/' in file_path:
            modules['services'].append(file_path)
        elif '/tests/' in file_path:
            modules['tests'].append(file_path)
        else:
            modules['root'].append(file_path)
    
    # Print modules
    print("\nМодули проекта:")
    for module, files in modules.items():
        if files:
            print(f"\n{module.upper()}:")
            for file in sorted(files):
                print(f"  - {file}")
    
    print("\n" + "=" * 50)
    print("Инструкции по установке:")
    print("1. Создайте виртуальное окружение Python 3.10+")
    print("2. Установите зависимости: pip install -r requirements.txt")
    print("3. Настройте файл .env на основе .env.example")
    print("4. Запустите бота: python app.py")
    print("=" * 50)

if __name__ == "__main__":
    print_project_structure()