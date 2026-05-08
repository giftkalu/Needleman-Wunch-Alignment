from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MATCH = 1
MISMATCH = -1
GAP = -2


def needleman_wunsch(seq1, seq2):
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        matrix[i][0] = i * GAP

    for j in range(cols):
        matrix[0][j] = j * GAP

    for i in range(1, rows):
        for j in range(1, cols):

            match_score = (
                MATCH if seq1[i - 1] == seq2[j - 1]
                else MISMATCH
            )

            diagonal = matrix[i - 1][j - 1] + match_score
            up = matrix[i - 1][j] + GAP
            left = matrix[i][j - 1] + GAP

            matrix[i][j] = max(diagonal, up, left)

    aligned1 = ""
    aligned2 = ""

    i = len(seq1)
    j = len(seq2)

    while i > 0 and j > 0:

        current = matrix[i][j]
        diagonal = matrix[i - 1][j - 1]
        up = matrix[i - 1][j]
        left = matrix[i][j - 1]

        if seq1[i - 1] == seq2[j - 1]:
            score = MATCH
        else:
            score = MISMATCH

        if current == diagonal + score:
            aligned1 = seq1[i - 1] + aligned1
            aligned2 = seq2[j - 1] + aligned2
            i -= 1
            j -= 1

        elif current == up + GAP:
            aligned1 = seq1[i - 1] + aligned1
            aligned2 = "-" + aligned2
            i -= 1

        else:
            aligned1 = "-" + aligned1
            aligned2 = seq2[j - 1] + aligned2
            j -= 1

    while i > 0:
        aligned1 = seq1[i - 1] + aligned1
        aligned2 = "-" + aligned2
        i -= 1

    while j > 0:
        aligned1 = "-" + aligned1
        aligned2 = seq2[j - 1] + aligned2
        j -= 1

    return {
        "score": matrix[-1][-1],
        "aligned1": aligned1,
        "aligned2": aligned2,
        "matrix": matrix
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/align", methods=["POST"])
def align():
    data = request.get_json()

    seq1 = data.get("seq1", "").upper()
    seq2 = data.get("seq2", "").upper()

    result = needleman_wunsch(seq1, seq2)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
