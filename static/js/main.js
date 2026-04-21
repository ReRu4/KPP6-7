document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const resultDiv = document.getElementById('result');
    const formData = new FormData(this);

    resultDiv.className = 'result hidden';
    resultDiv.textContent = '';

    try {
        const response = await fetch('/', { method: 'POST', body: formData });
        const data = await response.json();

        if (data.error) {
            resultDiv.className = 'result error';
            resultDiv.textContent = 'Ошибка: ' + data.error;
        } else {
            resultDiv.className = 'result';
            resultDiv.innerHTML =
                `<strong>Класс:</strong> ${data.class}<br>
                 <strong>Уверенность:</strong> ${(data.confidence * 100).toFixed(2)}%`;
        }
    } catch (err) {
        resultDiv.className = 'result error';
        resultDiv.textContent = 'Ошибка соединения: ' + err.message;
    }
});
