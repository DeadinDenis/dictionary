
# Admin page to manage words
from flask import abort

def register_admin_routes(app):
    @app.route('/admin')
    def admin():
        words = Word.query.order_by(Word.word).all()
        return render_template('admin.html', words=words)


    @app.route('/admin/add', methods=['GET', 'POST'])
    def admin_add():
        if request.method == 'POST':
            word = request.form.get('word', '').strip()
            definition = request.form.get('definition', '').strip()
            image = request.form.get('image', '').strip()
            examples = request.form.get('examples', '').strip()
            if word and definition:
                db.session.add(Word(word=word, definition=definition, image=image, examples=examples))
                db.session.commit()
                flash('Word added!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Both word and definition are required.', 'danger')
        return render_template('admin_add.html')


    @app.route('/admin/edit/<int:word_id>', methods=['GET', 'POST'])
    def admin_edit(word_id):
        word_obj = Word.query.get_or_404(word_id)
        if request.method == 'POST':
            word = request.form.get('word', '').strip()
            definition = request.form.get('definition', '').strip()
            image = request.form.get('image', '').strip()
            examples = request.form.get('examples', '').strip()
            if word and definition:
                word_obj.word = word
                word_obj.definition = definition
                word_obj.image = image
                word_obj.examples = examples
                db.session.commit()
                flash('Word updated!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Both word and definition are required.', 'danger')
        return render_template('admin_edit.html', word=word_obj)

    @app.route('/admin/delete/<int:word_id>', methods=['POST'])
    def admin_delete(word_id):
        word_obj = Word.query.get_or_404(word_id)
        db.session.delete(word_obj)
        db.session.commit()
        flash('Word deleted!', 'success')
        return redirect(url_for('admin'))


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-secret-key'
db = SQLAlchemy(app)


# Register admin routes after all dependencies are defined

# Admin routes will be added next

register_admin_routes(app)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # image filename or URL
    examples = db.Column(db.Text, nullable=True)      # example usages

    def first_letter(self):
        return self.word[0].upper() if self.word else ''


@app.route('/')
def index():
    letters = list(string.ascii_uppercase)
    slang_words = {letter: [] for letter in letters}
    for word in Word.query.order_by(Word.word).all():
        letter = word.first_letter()
        if letter in slang_words:
            slang_words[letter].append(word)
    return render_template('index.html', letters=letters, slang_words=slang_words)


@app.route('/word/<letter>/<word>')
def word_page(letter, word):
    word_obj = Word.query.filter(db.func.lower(Word.word) == word.lower(), db.func.substr(Word.word, 1, 1) == letter.upper()).first()
    return render_template('word.html', word=word_obj, letter=letter)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        words = Word.query.filter(Word.word.ilike(f'%{query}%')).order_by(Word.word).all()
        for w in words:
            results.append({'letter': w.first_letter(), 'word': w.word})
    return render_template('search.html', query=query, results=results)


# Admin routes will be added next

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)
