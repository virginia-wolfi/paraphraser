from flask import Flask, request, render_template

from form import SentenceInputForm
from functions import parse_sentence
from permuted_syntax_tree import PermutedSyntaxTree
from io import StringIO
import sys


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # Redirect stdout to capture printed output
    output = StringIO()
    sys.stdout = output
    form = SentenceInputForm(request.form)
    if request.method == "POST" and form.validate():
        sentence = form.sentence.data
        tree = parse_sentence(sentence)
        pst = PermutedSyntaxTree(tree)
        permutations = pst.get_permutations_as_string()
        tr = pst.tree
        # Get the captured output as a string

        return render_template(
            "index.html", tr=tr, sentence=sentence, permutations=permutations, form=form
        )
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
