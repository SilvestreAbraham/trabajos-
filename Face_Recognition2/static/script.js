const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultado = document.getElementById("resultado");
const ctx = canvas.getContext("2d");

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

setInterval(() => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imgData = canvas.toDataURL("image/jpeg");

    fetch("/reconocer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imgData })
    })
    .then(response => response.json())
    .then(data => {
        resultado.textContent = `👤 Reconocido: ${data.nombre}`;
    });
}, 3000);