from flask import Flask, request, render_template

from form import SentenceInputForm
from functions import parse_sentence
from permuted_syntax_tree import PermutedSyntaxTree


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    form = SentenceInputForm(request.form)
    if request.method == "POST" and form.validate():
        mode = form.mode.data
        sentence = form.sentence.data
        tree = sentence if mode == 'tree' else parse_sentence(sentence)

        try:
            pst = PermutedSyntaxTree(tree)
            permutations = pst.get_permutations_as_string()
            tree = pst.tree
        except Exception:
            exception = 'You provided an incorrect sentence'
            return render_template("index.html", exception=exception, form=form)

        return render_template(
            "index.html", tree=tree, sentence=sentence, permutations=permutations, form=form
        )

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
