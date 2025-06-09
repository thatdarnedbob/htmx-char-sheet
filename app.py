from flask import flash, Flask, redirect, render_template, request
from character_model import Character

app = Flask(__name__)

with open("secretkey.txt", "r") as f:
    app.secret_key = f.readlines()[0]

print("started!")

@app.route("/")
def index():
    return redirect("/characters")

@app.route("/characters")
def characters():
    search_term = request.args.get("q")
    if search_term is not None:
        characters_set = Character.search(search_term)
    else:
        characters_set = Character.all()
    return render_template("index.html", characters=characters_set)

@app.route("/characters/new", methods=['GET'])
def characters_new_get():
    return render_template("new.html", character=Character())

@app.route("/characters/new", methods=['POST'])
def characters_new_post():
    c = Character(  None,
                    request.form['name'],
                    request.form['caste'],
                    request.form['descriptor'],
                    request.form['gift'])
    if c.save():
        flash("Created new character!")
        return redirect("/characters")
    else:
        return render_template("new.html", character=c)
    
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
    c.update(request.form['name'],
             request.form['caste'],
             request.form['descriptor'],
             request.form['gift'])
    if c.save():
        flash("Updated character!")
        return redirect("/characters/" + str(id) )
    else:
        return render_template("edit.html", character=c)

@app.route("/characters/<id>/delete", methods=['POST'])
def character_delete(id=0):
    character = Character.find(id)
    character.delete()
    flash("Deleted Character!")
    return redirect("/characters")

app.run()