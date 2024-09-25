document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const pdfFile = document.getElementById("pdfFile").files[0];
    if (!pdfFile) {
        alert("Por favor, selecione um arquivo PDF.");
        return;
    }

    const formData = new FormData();
    formData.append("pdf", pdfFile);

    fetch("/process_pdf", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log(Object.keys(data))
        const resultadoDiv = document.getElementById("resultado");
        if (data.error) {
            resultadoDiv.textContent = data.error;
        } else {
            resultadoDiv.innerHTML = `
                <p><strong>Nota:</strong> ${data.nota}</p>
                <p><strong>Positivo:</strong> ${data.positivos}</p>
                <p><strong>Negativo:</strong> ${data.negativos}</p>
                <p><strong>Melhorias:</strong> ${data.melhorias}</p>
            `;
        }
    })
    .catch(error => {
        console.error("Erro:", error);
    });
});
