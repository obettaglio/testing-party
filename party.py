"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?

    >>> is_mel("Mel Melitpolski", "mel@ubermelon.com")
    True

    >>> is_mel("Mel Meltipolski", "mel@ubermelon.com")
    True

    >>> is_mel("Emvia", "letmecometoyourparty@please.com")
    False

    >>> is_mel("MEL", "mel@uerbmelon.com")
    True

    >>> is_mel("please", "MEL@UBERMELON.COM")
    True

    """

    return ((name.lower() == "mel melitpolski" or name.lower() == "mel")
            or email.lower() == "mel@ubermelon.com")


def most_and_least_common_type(treats):
    """Given list of treats, return {most, least} common types.

    >>> treats = []

    >>> most_and_least_common_type(treats)
    (None, None)

    >>> treats = [{'type': 'drink'},{'type': 'drink'}]

    >>> most_and_least_common_type(treats)
    ('drink', 'drink')

    >>> treats = [{'type': 'dessert'}, {'type': 'drink'}, {'type': 'drink'},\
                  {'type': 'drink'}, {'type': 'appetizer'}, {'type': 'appetizer'}]

    >>> most_and_least_common_type(treats)
    ('drink', 'dessert')

    >>> treats.append({'type':'appetizer'})

    >>> most_and_least_common_type(treats)
    ('drink', 'dessert')

    """

    types = {}
    treat_types = ["drink", "dessert", "appetizer"]

    # Count number of each type
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for ttype, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = ttype
        if least_count is None or count < least_count:
            least_count = count
            least_type = ttype

    if most_type == least_type and most_type is not None:
        treat_types.remove(most_type)
        least_type = treat_types[0] + " or " + treat_types[1]

    return (most_type, least_type)


def get_treats():
    """Get treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Agne'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats", methods=["GET", "POST"])
def show_treats():
    """Show treats people are bringing."""

    # Use request object method .methods() to give different behavior based on
    # GET or POST
    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)

    # Run only on POST request
    # treat = request.form.get("treat")
    # ttype = request.form.get("type")

    # if treat:
    #     flash("Thanks for adding " + treat)
    #     return redirect("/treats")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        session['name'] = name
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


@app.route("/add_treat")
def add_treat():
    """Allow adding a treat to the party's list"""
    return render_template("add_treat.html")

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run()
