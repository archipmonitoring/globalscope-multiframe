#!/usr/bin/env python3
"""
Agent Dependency Audit Script
==============================

Аналізує зв’язки між агентами в системі HoloMisha.
Виявляє:
- Циклічні залежності
- Надмірні зв’язки
- Відсутність модульності

Використання:
    python scripts/agent_dependency_audit.py
"""

import os
import ast
import json
from collections import defaultdict, deque
from typing import Dict, List, Set

# --- Налаштування ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
EXCLUDE_DIRS = {"__pycache__", "tests", "docs", "examples", "web_demo", "monitoring", "scripts"}
AGENT_KEYWORDS = ["agent", "engine", "orchestrator", "trainer", "analyzer"]

# --- Функції ---
def find_python_files(root_dir: str) -> List[str]:
    """Знаходить усі .py файли в директорії, крім виключень."""
    py_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def extract_imports(file_path: str) -> Set[str]:
    """Витягує імпорти з Python-файлу."""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            print(f"[!] Помилка синтаксису в {file_path}")
            return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports

def is_agent_module(module_name: str) -> bool:
    """Перевіряє, чи є модуль агентом."""
    return any(keyword in module_name.lower() for keyword in AGENT_KEYWORDS)

def build_dependency_graph(py_files: List[str]) -> Dict[str, Set[str]]:
    """Будує граф залежностей між модулями."""
    graph = defaultdict(set)
    module_map = {}  # module_name -> file_path

    # Створюємо мапу модулів
    for file in py_files:
        rel_path = os.path.relpath(file, PROJECT_ROOT)
        module_name = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")
        module_map[module_name] = file

    # Аналізуємо імпорти
    for file in py_files:
        rel_path = os.path.relpath(file, PROJECT_ROOT)
        module_name = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")
        imports = extract_imports(file)

        # Фільтруємо лише агенти
        if not is_agent_module(module_name):
            continue

        for imp in imports:
            if imp in module_map and is_agent_module(imp):
                graph[module_name].add(imp)

    return graph

def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Шукає циклічні залежності в графі."""
    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node: str, path: List[str]):
        if node in rec_stack:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            dfs(neighbor, path)

        path.pop()
        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles

def print_report(graph: Dict[str, Set[str]], cycles: List[List[str]]):
    """Виводить звіт про залежності."""
    print("\n=== 🧠 Аудит зв’язків між агентами ===\n")

    print("🔗 Усі зв’язки:")
    for module, deps in graph.items():
        if deps:
            print(f"  {module}")
            for dep in deps:
                print(f"    → {dep}")

    if cycles:
        print("\n🌀 Циклічні залежності:")
        for cycle in cycles:
            print("  → ".join(cycle))
    else:
        print("\n✅ Немає циклічних залежностей!")

    print("\n📊 Загальна статистика:")
    print(f"  Модулів: {len(graph)}")
    print(f"  Зв’язків: {sum(len(deps) for deps in graph.values())}")
    print(f"  Циклів: {len(cycles)}")

    # Якщо є цикли — повертаємо помилку
    if cycles:
        print("\n❌ Знайдено циклічні залежності! CI провалено.")
        exit(1)
    else:
        print("\n✅ Немає циклів. Архітектура чиста!")

# --- Головна функція ---
if __name__ == "__main__":
    print("🔍 Починаю аудит зв’язків між агентами...")
    py_files = find_python_files(SRC_DIR)
    graph = build_dependency_graph(py_files)
    cycles = find_cycles(graph)
    print_report(graph, cycles)