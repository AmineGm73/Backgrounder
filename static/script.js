const socket = io();

const playBtn = document.getElementById("play");
const stopBtn = document.getElementById("stop");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");

console.log("Logged in");

function playMusic() {
    socket.emit('playMusic');
    location.reload();
}

function stopMusic() {
    socket.emit("stopMusic");
    location.reload();
}

class MusicPlayer {
    constructor() {
        this.play = this.play.bind(this);
        this.playBtn = document.getElementById('play');
        this.playBtn.addEventListener('click', this.play);
        this.controlPanel = document.getElementById('control-panel');
        this.infoBar = document.getElementById('info');
    }

    play() {
        let controlPanelObj = this.controlPanel,
            infoBarObj = this.infoBar;
        Array.from(controlPanelObj.classList).find(function(element) {
            return element !== "active" ? controlPanelObj.classList.add('active') : controlPanelObj.classList.remove('active');
        });

        Array.from(infoBarObj.classList).find(function(element) {
            return element !== "active" ? infoBarObj.classList.add('active') : infoBarObj.classList.remove('active');
        });
    }
}

// Create an instance of the MusicPlayer class
const musicPlayer = new MusicPlayer();
