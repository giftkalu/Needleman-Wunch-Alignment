async function alignSequences() {

    const seq1 = document.getElementById("seq1").value;
    const seq2 = document.getElementById("seq2").value;

    const response = await fetch("/align", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            seq1,
            seq2
        })
    });

    const data = await response.json();

    let matrixHTML = "<table>";

    data.matrix.forEach(row => {
        matrixHTML += "<tr>";

        row.forEach(cell => {
            matrixHTML += `<td>${cell}</td>`;
        });

        matrixHTML += "</tr>";
    });

    matrixHTML += "</table>";

    document.getElementById("results").innerHTML = `
        <h2>Alignment Score: ${data.score}</h2>

        <p><strong>Sequence 1:</strong></p>
        <p>${data.aligned1}</p>

        <p><strong>Sequence 2:</strong></p>
        <p>${data.aligned2}</p>

        <h3>Scoring Matrix</h3>

        ${matrixHTML}
    `;
}
