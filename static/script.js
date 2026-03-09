document.getElementById('irisForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        sepal_length: document.getElementById("sepal_length").value,
        sepal_width: document.getElementById("sepal_width").value,
        petal_length: document.getElementById("petal_length").value,
        petal_width: document.getElementById("petal_width").value
    };

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("result").innerText = "Predicted Species: " + result.species;
    })
    .catch(err => {
        document.getElementById("result").innerText = "Error: " + err.message;
    });
});
