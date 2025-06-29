import json
import random
from paths_test import JSON_LOC


PAGE_SIZE = 10
ALIVE = ["Alive", None]
DEAD = ["Dead", None]

class Character:

    db = {}

    def __init__(self,  id=None,
                        name=None,
                        occupation=None,
                        debt=None,
                        hp=0,
                        str=0,
                        dex=0,
                        cha=0,
                        inventory=None,
                        oddity_1=None,
                        oddity_2=None,
                        player=None,
                        status=None):
        self.id = id
        self.name = name
        self.occupation = occupation
        self.debt = debt
        if hp==0:
            self.hp = random.randint(1,6)
        else:
            self.hp = hp
        if str == 0 or dex == 0 or cha ==0:
            self.str, self.dex, self.cha = Character.randomStats()
        else:
            self.str, self.dex, self.cha = str, dex, cha
        self.inventory = inventory
        self.oddity_1 = oddity_1
        self.oddity_2 = oddity_2
        self.player = player
        if status is None:
            self.status = ALIVE
        else:
            self.status = status
        self.errors = {}

    def delete(self):
        del Character.db[self.id]
        Character.save_db()

    def save(self):
        if not self.validate():
            print("not valid")
            print(self.errors)
            return False
        if self.id is None:
            if len(Character.db) == 0:
                max_id = 0
            else:
                max_id = max(character.id for character in Character.db.values())
            self.id = max_id + 1
            Character.db[self.id] = self
        Character.save_db()
        return True
    
    def update(self,    name,
                        occupation,
                        debt,
                        hp,
                        str,
                        dex,
                        cha,
                        inventory,
                        oddity_1,
                        oddity_2,
                        player,
                        status):
        print('inside update')
        self.name = name
        self.occupation = occupation
        self.debt = debt
        self.hp = hp
        self.str = str
        self.dex = dex
        self.cha = cha
        self.inventory = inventory
        self.oddity_1 = oddity_1
        self.oddity_2 = oddity_2
        self.player = player
        if status is not None:
            self.status = status

    def validate(self):
        self.errors = {}
        if not self.name:
            self.errors['name'] = "Name Required"
        if not self.occupation or not self.occupation[0]:
            self.errors['occupation'] = "Occupation Required"
        if not self.oddity_1 or not self.oddity_1[0]:
            self.errors['oddity_1'] = "Don't delete that! That part rules"
        if not self.oddity_2 or not self.oddity_2[0]:
            self.errors['oddity_2'] = "Don't delete that! That part rules"
        if not self.player:
            self.errors['player'] = "This would be you..."
        if not self.status:
            print(self.status)
            self.errors['status'] = "Current status required"
        return len(self.errors) == 0
    
    @classmethod
    def all(cls, page=1):
        page = int(page)
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        return list(cls.db.values())[start:end]

    @classmethod
    def find(cls, id):
        id = int(id)
        c = cls.db.get(id)
        if c is not None:
            c.errors = {}
        return c

    @staticmethod
    def randomStats():
        str = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        dex = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        cha = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        return str, dex, cha

    @classmethod    
    def search(cls, search_term):
        results = []
        for c in cls.db.values():
            match_name = c.name is not None and search_term in c.name
            match_occupation = c.occupation is not None and search_term in c.occupation[0]
            match_debt = c.debt is not None and search_term in c.debt[0]
            match_oddity_1 = c.oddity_1 is not None and search_term in c.oddity_1[0]
            match_oddity_2 = c.oddity_2 is not None and search_term in c.oddity_2[0]
            match_player = c.player is not None and search_term in c.player
            match_status = c.status is not None and search_term in c.status[0]
            if (match_name or 
                match_occupation or 
                match_debt or 
                match_oddity_1 or
                match_oddity_2 or
                match_player or
                match_status):
                results.append(c)
        return results

    @classmethod
    def load_db(cls):
        with open(JSON_LOC, "r") as character_file:
            characters = json.load(character_file)
            cls.db.clear()
            for c in characters:
                cls.db[c['id']] = Character(c['id'], 
                                            c['name'], 
                                            c['occupation'], 
                                            c['debt'],
                                            c['hp'],
                                            c['str'],
                                            c['dex'],
                                            c['cha'],
                                            c['inventory'],
                                            c['oddity_1'],
                                            c['oddity_2'],
                                            c['player'],
                                            c['status'])

    @staticmethod
    def save_db():
        out_arr = [c.__dict__ for c in Character.db.values()]
        with open(JSON_LOC, "w") as f:
            json.dump(out_arr, f, indent=2)