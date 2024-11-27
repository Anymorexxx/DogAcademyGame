import random

def generate_map(level):
    """Генерация карты уровня."""
    num_obstacles = random.randint(3, 6)
    map_data = []
    for _ in range(num_obstacles):
        map_data.append({
            "type": "question",
            "difficulty": level,
            "position": (random.randint(0, 19), random.randint(0, 10))  # Позиция на сетке
        })
    return map_data
