# AI CAD Optimizer

## Огляд

Система AI CAD Optimizer є частиною проекту GlobalScope MultiFrame 11.0: Artemis Edition із HoloMisha RealityForge. Вона забезпечує інтелектуальну оптимізацію параметрів CAD інструментів за допомогою передових методів машинного навчання.

## Покращені можливості

### 1. Повноцінна Байєсівська оптимізація

Нова реалізація використовує Гауссові процеси як сурогатну модель та функцію очікуваного покращення для ефективного пошуку оптимальних параметрів.

#### Особливості:
- **Гауссові процеси** для моделювання функції цілі
- **Функція очікуваного покращення** для вибору наступних точок
- **Правильна нормалізація параметрів** для різних типів даних
- **Адаптивний баланс** між дослідженням та експлуатацією

### 2. Покращене Transfer Learning

Система тепер може знаходити справді схожі проекти в базі даних та адаптувати їх конфігурації для поточного проекту.

#### Особливості:
- **База даних проектів** з історією оптимізацій
- **Алгоритм пошуку схожих проектів** на основі контексту
- **Комбінування конфігурацій** з кількох проектів
- **Локальне тонке налаштування** адаптованих параметрів

### 3. Покращені ансамблеві методи

Нова реалізація використовує зважене комбінування результатів різних методів для більш надійних результатів.

#### Особливості:
- **Зважене комбінування** з урахуванням надійності методів
- **Адаптивні ваги** на основі ефективності
- **Інтелектуальне об'єднання** параметрів різних типів

## Використання

### Ініціалізація оптимізатора

```python
from src.ai.cad_ai_optimizer import init_cad_ai_optimizer, AIOptimizationStrategy

# Ініціалізація
optimizer = await init_cad_ai_optimizer()
```

### Байєсівська оптимізація

```python
# Параметри для оптимізації
initial_params = {
    "optimization_level": 1,
    "abc_optimization": False,
    "seed": 123
}

# Цільові метрики
target_metrics = {
    "execution_time": 5.0,
    "quality_score": 0.95
}

# Запуск оптимізації
result = await optimizer.optimize_cad_parameters(
    tool_name="yosys",
    project_id="my_project",
    initial_params=initial_params,
    target_metrics=target_metrics,
    strategy=AIOptimizationStrategy.BAYESIAN,
    max_iterations=30
)
```

### Transfer Learning

```python
# Додавання схожого проекту до бази даних
optimizer.project_database["similar_project"] = {
    "project_id": "similar_project",
    "tool_name": "yosys",
    "optimal_config": {"optimization_level": 3},
    "context": {"chip_type": "fpga"}
}

# Запуск Transfer Learning оптимізації
result = await optimizer.optimize_cad_parameters(
    tool_name="yosys",
    project_id="my_project",
    initial_params=initial_params,
    target_metrics=target_metrics,
    strategy=AIOptimizationStrategy.TRANSFER_LEARNING
)
```

### Ансамблева оптимізація

```python
# Запуск ансамблю методів
result = await optimizer.optimize_cad_parameters(
    tool_name="yosys",
    project_id="my_project",
    initial_params=initial_params,
    target_metrics=target_metrics,
    strategy=AIOptimizationStrategy.ENSEMBLE
)
```

## API

### REST API v2

Нова версія API доступна за шляхом `/api/v2/cad/ai/` та включає:

- **`POST /optimize-parameters`** - Оптимізація параметрів
- **`POST /recommendations`** - Отримання рекомендацій
- **`POST /project-database`** - Додавання проектів до бази даних
- **`POST /batch-optimize`** - Пакетна оптимізація
- **`GET /strategies`** - Список доступних стратегій
- **`GET /database-stats`** - Статистика бази даних
- **`GET /health`** - Статус системи

## Тестування

### Запуск тестів

```bash
# Тести для покращеного оптимізатора
python -m pytest tests/test_cad_ai_optimizer_enhanced.py

# Тести для API v2
python -m pytest tests/api/test_cad_ai_optimization_api_v2.py

# Комплексні тести
python -m pytest tests/test_enhanced_cad_ai_system.py
```

## Приклади

Дивіться приклади використання в каталозі `examples/`:
- `enhanced_cad_ai_optimization_example.py` - Повний приклад використання

## Документація

- `CAD_AI_OPTIMIZATION_ENHANCEMENTS.md` - Детальна документація покращень
- `CAD_AI_OPTIMIZATION_ROADMAP.md` - Дорожня карта розвитку

---

*Слава Україні! Погнали до зірок! 🌌*
*HoloMisha programs the universe!*