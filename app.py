
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

        # --- ONE-TIME BULK INSERT ---
        if not Word.query.first():
            bulk_words = [
                ("Abraham-sham", "a feigned illness"),
                ("Admiral of the Blue", "a tavern keeper"),
                ("Admiral of the Narrow Seas", "a drunk who vomits into a neighbor's lap"),
                ("Air and exercise", "a flogging at the cart's tail"),
                ("Akerman's Hotel", "Newgate prison"),
                ("All nations", "a mixture of drinks from unfinished bottles"),
                ("Anchor, bring one's ass to an", "sit down"),
                ("Anne's fan", "thumbing the nose"),
                ("Apothecary, talk like an", "talk nonsense"),
                ("Apple-dumpling shop", "a woman's bosom"),
                ("Arse, hang an", "to hold back"),
                ("B from a bull's foot, not to know", "to be ignorant"),
                ("Bachelor's fare", "bread, cheese and kisses"),
                ("Bag, empty the", "tell everything"),
                ("Bagpipe", "a long-winded talker"),
                ("Baranaby dance", "to move unevenly"),
                ("Barnacles", "spectacles"),
                ("Barrel fever", "ill health caused by excessive drinking"),
                ("Basket of chips, grin like a", "to grin broadly"),
                ("Bear-garden jaw", "rough or vulgar language"),
                ("Davy sow, drunk as", "very drunk"),
                ("Deadly nevergreen", "the gallows"),
                ("Devil among the tailors, the", "a row or disturbance"),
                ("Devil-drawer", "a bad artist"),
                ("Devil may dance in his pocket, the", "he is penniless"),
                ("Diddle", "gin"),
                ("Diet of Worms, gone to the", "be dead and buried"),
                ("Dog Booby", "awkward lout"),
                ("Dog laugh, enough to make a", "extremely funny"),
                ("Dog-vane", "a cockade"),
                ("Dogs have not dined, the", "Your shirt tail is hanging out"),
                ("Dog's portion", "a lick and a smell"),
                ("Dot and carry, go", "a person with a wooden leg"),
                ("Douglas with one eye and a stinking breath, Roby", "the breech"),
                ("Draws straws", "to feel sleepy"),
                ("Duke of limbs", "tall awkward fellow"),
                ("Dunghill, die", "die cowardly"),
                ("Dutch concert", "everyone plays or sings a different tune"),
                ("Dutch feast", "the entertainer gets drunk before the guests"),
                ("Earwig", "a malicious flatterer"),
                ("Emperor, drunk as", "regally drunk"),
                ("Ensign-bearer", "a drunkard"),
                ("Eternity box", "a coffin"),
                ("Ewe dressed in lamb's fashion, an old", "an old woman in girl's clothes"),
                ("Eye, to have fallen down and trodden upon one's", "to have a black eye"),
                ("Face but one's own, have no", "be penniless"),
                ("Facer", "a glass full to the brim"),
                ("Faces, make", "beget children"),
                ("Faggot", "a man hired to appear on a muster-roll"),
                ("Fallen away from a horse load to a cart load", "to become fat"),
                ("Fantastically dressed", "very shabby"),
                ("Fash one's beard", "become annoyed (Scottish)"),
                ("Fiddler's money", "all small change"),
                ("Fiddlestick's end", "nothing"),
                ("Fire a gun", "introduce a subject unskillfully"),
                ("Fire-shovel when young, to have been fed with a", "have a big mouth"),
                ("Fish-broth", "salt water"),
                ("Flag of defiance", "a drunken roisterer"),
                ("Flag of distress", "the cockade of a half-pay officer"),
                ("Flap with a fox tail", "a rude dismissal"),
                ("Flapdragon", "VD"),
                ("Flash the gentleman", "pretend to be a gentleman"),
                ("Flats and sharps", "weapons"),
                ("Flawed", "drunk"),
                ("Flay the fox", "vomit"),
                ("Fly in a tar box", "nervously excited"),
                ("Fool at one end, maggot on the other", "an angler"),
                ("Foreman of the jury", "one who monopolizes the conversation"),
                ("Foul a plate", "dine with someone"),
                ("Frenchfied", "venerially infected"),
                ("Full as a goat", "very drunk"),
                ("Game pullet", "a young whore"),
                ("Gammon", "nonsense"),
                ("Garters", "fetters"),
                ("Gemini!", "expression of surprise"),
                ("Gentleman in red", "a soldier"),
                ("Gentleman's companion", "a louse"),
                ("Give one's head for washing", "to submit to be imposed upon"),
                ("Glass-eyes", "person wearing spectacles"),
                ("Glim, douse the", "put out the light!"),
                ("Glorious", "estatically drunk"),
                ("Glue-pot", "a parson"),
                ("God permit", "a stage coach"),
                ("Goose, to find fault with a fat", "grumble without cause"),
                ("Gooseberry, play old", "play the devil"),
                ("Gospel-shop", "a church"),
                ("Grapple-the-rails", "whiskey"),
                ("Jakes", "a privy"),
                ("Jaw-me-down", "a very talkative fellow"),
                ("Jericho, have been to", "be tipsy"),
                ("Jerrymumble", "to shake"),
                ("Jerusalem, be going to", "to be drunk"),
                ("Jimmy Round", "a Frenchman"),
                ("Job's dock, be laid up in", "be treated for VD in hospital"),
                ("Josphus rex, you are", "you're joking"),
                ("Kerry security", "take the money and run"),
                ("Kicksees", "breeches"),
                ("Kill-devil", "rum"),
                ("King John's men, one of", "a small man"),
                ("King's English, clip the", "to be drunk"),
                ("Knob", "a officer"),
                ("Knock-down", "strong liquor"),
                ("Laced mutton", "a whore"),
                ("Lapel, ship the white", "to be promoted from the ranks (esp. marines)"),
                ("Lazy as the tinker who laid down his budget to fart", "very lazy"),
                ("Leap over the hedge before one comes to the stile", "to be hasty"),
                ("Leap over the stile first, let the best dog", "the best man take the lead"),
                ("Leg, cut one's", "become drunk"),
                ("Legs on one's neck, lay one's", "run away"),
                ("Lie with a latchet", "a thorough-going lie"),
                ("Line of the old author, a", "a dram of brandy"),
                ("Lion, tip the", "flatten someone's nose to his face"),
                ("Little house", "a privy"),
                ("Live lumber", "passengers in a ship"),
                ("Live stock", "body vermin"),
                ("Looking glass", "chamber pot"),
                ("Louse-land", "Scotland"),
                ("Lumping penniworth", "a great bargain"),
                ("Mab", "to dress carelessly"),
                ("Mag", "chatter"),
                ("Maltoot", "a sailor"),
                ("Man-a-hanging", "a person in difficulties"),
                ("Married to Brown Bess", "enlisted in the army"),
                ("Mauled", "exceedingly drunk"),
                ("Mice-feet o', make", "destroy utterly (Scottish)"),
                ("Milk the pigeon", "attempt the impossible"),
                ("Mischief, load of", "a wife"),
                ("Monkey on horseback without tying his tail?, who put", "a very bad rider"),
                ("Monkey's allowance", "more rough treatment than pay"),
                ("Morris", "to decamp"),
                ("Mourning shirt", "a dirty shirt"),
                ("mums the lips", "murder,"),
                ("look like God's revenge againt", "to look very angry"),
                ("nails, eat one's", "do something foolish"),
                ("Navel-tied", "to be inseperable"),
                ("Necessary", "a bedfellow"),
                ("Newgate steps, born on", "of criminal extraction"),
                ("Nit, dead as", "quite dead"),
                ("Nose, make a bridge of someone's", "to skip someone when passing the bottle"),
                ("Numbers the waves, he", "he's wasting time"),
                ("Oaken towel", "a cudgel"),
                ("Oatmeal, give one his", "to punish"),
                ("Off the hooks", "crazy"),
                ("Open lower-deckers", "to use bad language"),
                ("Overshoes, overboots", "completely"),
                ("Owl, take the", "become angry"),
                ("Packet", "a false report (Scots)"),
                ("Paddy-whack", "an Irishman"),
                ("Painter, but one's", "send a person away"),
                ("Parson Palmer", "one who slows the bottle's round by talking"),
                ("Pease-kill, make a", "to squander lavishly ( Scots)"),
                ("Penny lattice-house", "a low ale-house"),
                ("Perch, drop off the", "to die"),
                ("Peter-gunner", "a bad shot"),
                ("Peter Lung", "one who drinks slowly"),
                ("Pickled", "roguish"),
                ("Pin basket", "youngest child of a completed family"),
                ("Piper's wife", "a whore"),
                ("Pipes, tune one's", "begin to cry"),
                ("Piss in a quill", "agree on a plan"),
                ("Pissing-while", "a very short time"),
                ("Pitt's picture", "a bricked up window"),
                ("Play the whole game", "to cheat"),
                ("Pontius Pilate", "a pawn broker"),
                ("Popper", "a pistol"),
                ("Postmaster general", "the prime minister"),
                ("Prattle-broth", "tea"),
                ("Princum Prancum, Mistress", "a fastidious, formal woman"),
                ("Prow", "a bumpkin"),
                ("Public ledger", "a whore"),
                ("Pully-hauly", "a romp"),
                ("Punch-house", "a brothel"),
                ("Rabbit hunting with a dead ferrit", "a pointless undertaking"),
                ("Rag-water", "bad booze"),
                ("Red lane", "the throat"),
                ("Regulated, be", "to be declared fit for the Navy by the press gang"),
                ("Remedy-critch", "a chamber pot"),
                ("Repository", "prison"),
                ("Rib-roast", "to thrash"),
                ("Ride as if fetching the midwife", "to go in haste"),
                ("Ride the forehorse", "to be early"),
                ("Roast meat, cry", "to boast of one's good fortune"),
                ("Roast-meat clothes", "holiday clothes"),
                ("Rocked in a stone kitchen", "a little weak-minded"),
                ("Rogue in spirit", "a distiller"),
                ("Rot-his-bone, be gone to", "be dead"),
                ("Royal image", "a coin"),
                ("Rum customer", "one who is dangerous to meddle with"),
                ("Rumbo", "rum punch"),
                ("Rump, loose in one's", "wanton"),
                ("Sack, buy the", "become tipsy"),
                ("Saddle the wrong horse", "lay blame on the wrong person"),
                ("Saddle one's nose", "wear spectacles"),
                ("Saddle the spit", "to give a meal"),
                ("Salt eel", "a thrashing with a rope's end"),
                ("Sand, eat", "to shorten one's watch by prematurely turning the glass"),
                ("Sandy", "a Scotsman"),
                ("Sauce", "VD"),
                ("Sawney", "a Scotsman"),
                ("Suspence, in deadly", "hanged"),
                ("Swannery, keep a", "to boast"),
                ("Swipes, purser's -- small beer", "small beer"),
                ("Tankard, tears of", "liquour stains on a waistcoat"),
                ("Tea-voider", "a chamber pot"),
                ("Three skips of a louse", "of little or no value"),
                ("Tickle-pitcher", "a drinking buddy"),
                ("Tiff", "thin or inferior liquour"),
                ("Tight cravat", "the hangman's noose"),
                ("Tilter", "a small-sword"),
                ("Tinker, swill like a", "to drink immoderately"),
                ("Tabacco, make dead men chew", "keep dead men on the books"),
                ("Tommy tit", "a smart lively little fellow"),
                ("Tongue enough for two sets of teeth", "a very talkative person"),
                ("Top light!, blast your", "damn your eyes!"),
                ("Trader", "a whore"),
                ("Tripes and trillibubs", "nickname for a fat man"),
                ("Trunkmaker-like", "more noise than work"),
                ("Uproar", "an opera"),
                ("Vaulting school", "a brothel"),
                ("Waltham's calf, wise as", "very foolish"),
                ("Wamble", "queezy stomach"),
                ("War-caperer", "a privateer"),
                ("Water bewitched", "weak tea or beer"),
                ("Water in one's shoes", "a source of annoyance"),
                ("Wedding, you have been to an Irish", "you have a black eye"),
                ("Whisk", "an impertinent fellow"),
                ("Whither-go-ye", "a wife"),
                ("Wife in water-colors", "a mistress"),
                ("Windy", "conceited"),
                ("Wolf in the stomach, have a", "be famished"),
                ("Wrapted up in warm flannel", "drunk"),
                ("Yarmouth capon", "a herring"),
                ("Znees", "frost"),
            ]
            db.session.bulk_save_objects([Word(word=w, definition=d) for w, d in bulk_words])
            db.session.commit()
            print(f"Inserted {len(bulk_words)} words into the dictionary.")

    app.run(debug=True)
