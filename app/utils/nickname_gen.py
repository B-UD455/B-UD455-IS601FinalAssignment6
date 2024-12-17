'''
from builtins import str
import random


def generate_nickname() -> str:
    """Generate a URL-safe nickname using adjectives and animal names."""
    adjectives = ["clever", "jolly", "brave", "sly", "gentle"]
    animals = ["panda", "fox", "raccoon", "koala", "lion"]
    number = random.randint(0, 999)
    return f"{random.choice(adjectives)}_{random.choice(animals)}_{number}"
'''

import random
import string

def generate_nickname(seed: str = None) -> str:
    """Generate a URL-safe nickname using adjectives, animals, and an optional seed for consistency."""
    adjectives = ["clever", "jolly", "brave", "sly", "gentle", "wild", "swift", "happy", "loyal", "fierce"]
    animals = ["panda", "fox", "raccoon", "koala", "lion", "eagle", "tiger", "wolf", "bear", "shark"]
    
    # Use the seed if provided to generate a consistent nickname (useful for user-related scenarios)
    if seed:
        random.seed(seed)
    
    # Generate the nickname with random adjective, animal, and number
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.randint(0, 999)
    
    # Construct the nickname
    nickname = f"{adjective}_{animal}_{number}"
    
    # Ensure the nickname is URL-safe by replacing spaces with underscores and removing unwanted characters
    return ''.join(char if char in string.ascii_letters + string.digits + "_" else "" for char in nickname)

