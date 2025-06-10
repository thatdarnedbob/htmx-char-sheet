import json

PAGE_SIZE = 100

class Character:

    db = {}

    def __init__(self, id=None, name=None, caste=None, descriptor=None, gift=None):
        self.id = id
        self.name = name
        self.caste = caste
        self.descriptor = descriptor
        self.gift = gift
        self.errors = {}

    def delete(self):
        del Character.db[self.id]
        Character.save_db()

    def save(self):
        if not self.validate():
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
    
    def update(self, name, caste, descriptor, gift):
        self.name = name
        self.caste = caste
        self.descriptor = descriptor
        self.gift = gift

    def validate(self):
        if not self.gift:
            self.errors['gift'] = "Gift Required"
        existing_character = next(filter(
                lambda c: c.id != self.id and c.gift == self.gift,
                Character.db.values()),
            None)
        if existing_character:
            self.errors['gift'] = "Gift Must Be Unique"
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
    @classmethod    
    def search(cls, search_term):
        results = []
        for c in cls.db.values():
            match_name = c.name is not None and search_term in c.name
            match_caste = c.caste is not None and search_term in c.caste
            match_gift = c.gift is not None and search_term in c.gift
            match_descriptor = c.descriptor is not None and search_term in c.descriptor
            if match_name or match_caste or match_gift or match_descriptor:
                results.append(c)
        return results

    @classmethod
    def load_db(cls):
        print("loading")
        with open("characters.json", "r") as character_file:
            print("file open")
            characters = json.load(character_file)
            cls.db.clear()
            for c in characters:
                print(c)
                cls.db[c['id']] = Character(c['id'], 
                                            c['name'], 
                                            c['caste'], 
                                            c['descriptor'], 
                                            c['gift'])
        print("file complete")

    @staticmethod
    def save_db():
        out_arr = [c.__dict__ for c in Character.db.values()]
        with open("characters.json", "w") as f:
            json.dump(out_arr, f, indent=2)