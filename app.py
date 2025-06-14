from flask import flash, Flask, redirect, render_template, request
from character_model import Character, ALIVE, DEAD
import datagenerator
from paths_test import SECRET_KEY

Character.load_db()

app = Flask(__name__)

with open(SECRET_KEY, "r") as f:
    app.secret_key = f.readlines()[0]

@app.route("/")
def index():
    return render_template('front.html')

@app.route("/characters")
def characters():
    search_term = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search_term is not None:
        characters_set = Character.search(search_term)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template('partials/rows.html', characters=characters_set, page=page)
    else:
        characters_set = Character.all(page)
    return render_template("index.html", characters=characters_set, page=page)

@app.route("/characters/new", methods=['GET'])
def characters_new_get():
    character = datagenerator.randomCharacter()
    if character.save():
        flash("Created new character!")
    return render_template("newnew.html", character=character)

@app.route("/characters/new", methods=['POST'])
def characters_new_post():
    print("saw new post")
    print(request.form)
    character = Character.find(request.form['id'])
    print('got to update')
    character.update(name=request.form['name'],
                        occupation=character.occupation,
                        debt=character.debt,
                        hp=character.hp,
                        str=character.str,
                        dex=character.dex,
                        cha=character.cha,
                        inventory=request.form['inventory'],
                        oddity_1=[character.oddity_1[0], request.form['oddity_1_response']],
                        oddity_2=[character.oddity_2[0], request.form['oddity_2_response']],
                        player=request.form['player'],
                        status=ALIVE)
    print('got to conditional')
    if character.save():
        print('did save')
        flash("Created new character!")
        return redirect("/characters")
    else:
        print('did not save')
        return render_template("new.html", character=character)
    
@app.route("/characters/<id>")
def character_view(id=0):
    character = Character.find(id)
    return render_template("show.html", character=character)

@app.route("/characters/<id>/edit", methods=['GET'])
def character_edit_get(id=0):
    character = Character.find(id)
    return render_template("edit.html", character=character)

@app.route("/characters/<id>/edit", methods=['POST'])
def character_edit_post(id=0):
    c = Character.find(id)
    c.update(   name=request.form['name'],
                occupation=[request.form['occupation_title'], request.form['occupation_desc']],
                debt=None,
                hp=request.form['hp'],
                str=request.form['str'],
                dex=request.form['dex'],
                cha=request.form['cha'],
                inventory=request.form['inventory'],
                oddity_1=[request.form['oddity_1_question'], request.form['oddity_1_response']],
                oddity_2=[request.form['oddity_2_question'], request.form['oddity_2_response']],
                player=request.form['player'],
                status=None)
    if c.save():
        flash("Updated character!")
        return redirect("/characters/" + str(id) )
    else:
        return render_template("edit.html", character=c)
    
@app.route("/characters/<id>/name", methods=['GET'])
def character_name_get(id=0):
    c = Character.find(id)
    c.name = request.args.get('name')
    c.validate()
    return c.errors.get('name') or ''

@app.route("/characters/new/name", methods=['GET'])
def character_name_check():
    c = Character()
    c.name = request.args.get('name')
    c.validate()
    return c.errors.get('name') or ''

@app.route("/characters/<id>", methods=['DELETE'])
def character_delete(id=0):
    character = Character.find(id)
    character.delete()
    flash("Deleted character!")
    return redirect("/characters", 303)

@app.route("/characters/<id>/kill", methods=['GET'])
def character_request_death_info(id=0):
    character = Character.find(id)
    character.status[0] = DEAD[0]
    Character.save_db()
    return render_template("death.html", character=character)

@app.route("/characters/<id>/kill", methods=['POST'])
def character_kill(id=0):
    character = Character.find(id)
    character.status[1] = request.form['cause_of_death']
    Character.save_db()
    return redirect("/characters", 303)

if __name__ == '__main__':
    app.run()