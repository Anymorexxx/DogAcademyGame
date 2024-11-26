import random

def generate_map(level):
    """Генерация карты уровня."""
    num_obstacles = random.randint(3, 6)
    map_data = []
    for i in range(num_obstacles):
        map_data.append({
            "type": "question",
            "difficulty": level,
            "position": random.randint(1, 100)
        })
    return map_data
