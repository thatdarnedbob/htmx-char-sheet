from character_model import Character
import random

NUM_CHARACTERS = 450

NAME_PHONEMES = ['ab', 'ad', 'ag', 'ko', 'lor', 'lak', 'bat', 'zor', 'xo', 'ox', 'oz', 'ba', 'da', 'gad', 'rat', 'gor']

CASTES = ['Warrior', 'Wizard', 'Rogue', 'Thief', 'Barbarian', 'Berzerker', 'Cleric', 'Priest']

ADJS = ['Strong', 'Fierce', 'Wise', 'Smart', 'Cunning', 'Depraved', 'Cruel', 'Heroic']

VERBS = ['Fights', 'Suffers', 'Laughs', 'Learns', 'Boils', 'Stews', 'Sleeps']

ITEM_ADJS = ['Golden', 'Silver', 'Brazen', 'Enormous', 'Tiny', 'Corroded']

ITEM_NOUNS = ['Teapot', 'Sword', 'Crown', 'Breastplate', 'Dagger', 'Coin']

def randomCharacter():
    caste = randomCaste()
    c = Character(  name=randomName(),
                    caste=caste,
                    descriptor=randomDescriptor(caste),
                    gift=randomGift())
    return c

def randomName():
    return ''.join(random.sample(NAME_PHONEMES, 3)).capitalize()

def randomCaste():
    return random.choice(CASTES)

def randomDescriptor(caste):
    return f"A {randomAdj()} {caste} who {randomVerb()}".capitalize()

def randomAdj():
    return random.choice(ADJS)

def randomVerb():
    return random.choice(VERBS)

def randomGift():
    return f"A {randomItemAdj()} {randomItemNoun()}"

def randomItemAdj():
    return random.choice(ITEM_ADJS)

def randomItemNoun():
    return random.choice(ITEM_NOUNS)


Character.db.clear()

for i in range(NUM_CHARACTERS):
    r = randomCharacter()
    while not r.validate():
        r.name = randomName()
    r.save()

Character.save_db()