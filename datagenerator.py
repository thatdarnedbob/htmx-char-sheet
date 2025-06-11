from character_model import Character
import random

NUM_OCCUPATIONS = 108
NUM_CHARACTERS = 450
OCCUPATION_OFFSET = 27
OO = OCCUPATION_OFFSET

secret_text = ''

with open('eb.txt', 'r') as f:
    secret_text = f.readlines()

def randomCharacter():
    o_num = random.randrange(NUM_OCCUPATIONS)
    c = Character(  name=grabName(o_num),
                    occupation=grabOccupation(o_num),
                    debt=grabDebt(o_num),
                    inventory=grabInventory(o_num),
                    oddity_1=grabOddity1(o_num),
                    oddity_2=grabOddity2(o_num),
                    player="TEST")

    return c

def grabName(base):
    names = secret_text[base * OO + 3].split(': ', maxsplit=1)[1]
    names = names.rstrip('.')
    names = names.split(', ')
    return random.choice(names).capitalize().rstrip()

def grabOccupation(base):
    return [secret_text[base * OO].split('. ', maxsplit=1)[1].rstrip(),
            secret_text[base * OO + 1].rstrip()]
    
def grabDebt(base):
    return secret_text[base * OO + 6].rstrip().split(': ', maxsplit=1)

def grabInventory(base):
    return secret_text[base * OO + 9].rstrip()

def grabOddity1(base):
    choice = random.randrange(6)
    return [secret_text[base * OO + 11].rstrip(),
            secret_text[base * OO + 12 + choice][3:].rstrip()]

def grabOddity2(base):
    choice = random.randrange(6)
    return [secret_text[base * OO + 19].rstrip(),
            secret_text[base * OO + 20 + choice][4:].rstrip()]

Character.db.clear()

for i in range(NUM_CHARACTERS):
    r = randomCharacter()
    if not r.validate():
        raise Exception(r.errors)
    r.save()

Character.save_db()