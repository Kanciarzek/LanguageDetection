const recordAudio = () =>
    new Promise(async resolve => {
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        const start = () => {
            audioChunks = [];
            mediaRecorder.start();
        };

        const stop = () =>
            new Promise(resolve => {
                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks);
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    const play = () => audio.play();
                    resolve({audioChunks, audioBlob, audioUrl, play});
                });

                mediaRecorder.stop();
            });

        resolve({start, stop});
    });
const sleep = time => new Promise(resolve => setTimeout(resolve, time));

const recordButton = document.querySelector('#record');
const stopButton = document.querySelector('#stop');
const playButton = document.querySelector('#play');
const sendButton = document.querySelector('#send');

let recorder;
let audio;

recordButton.addEventListener('click', async () => {
    recordButton.setAttribute('disabled', true);
    stopButton.removeAttribute('disabled');
    playButton.setAttribute('disabled', true);
    if (!recorder) {
        recorder = await recordAudio();
    }
    recorder.start();
});

stopButton.addEventListener('click', async () => {
    recordButton.removeAttribute('disabled');
    stopButton.setAttribute('disabled', true);
    playButton.removeAttribute('disabled');
    playButton.removeAttribute('disabled');
    sendButton.removeAttribute('disabled');
    audio = await recorder.stop();

});

sendButton.addEventListener('click', () => {

})

playButton.addEventListener('click', () => {
    audio.play();
});
