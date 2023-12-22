socket = io();

const playBtn = document.getElementById("playBtn");
const stopBtn = document.getElementById("stopBtn");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");


console.log("Logged in");


function playMusic(){
    socket.emit('playMusic');
    location.reload()
}

function stopMusic(){
    socket.emit("stopMusic")
    location.reload()
}