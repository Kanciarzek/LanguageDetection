// Convert an AudioBuffer to a Blob using WAVE representation
function bufferToWave(abuffer, len) {
    var numOfChan = abuffer.numberOfChannels,
        length = len * numOfChan * 2 + 44,
        buffer = new ArrayBuffer(length),
        view = new DataView(buffer),
        channels = [], i, sample,
        offset = 0,
        pos = 0;

    // write WAVE header
    setUint32(0x46464952);                         // "RIFF"
    setUint32(length - 8);                         // file length - 8
    setUint32(0x45564157);                         // "WAVE"

    setUint32(0x20746d66);                         // "fmt " chunk
    setUint32(16);                                 // length = 16
    setUint16(1);                                  // PCM (uncompressed)
    setUint16(numOfChan);
    setUint32(abuffer.sampleRate);
    setUint32(abuffer.sampleRate * 2 * numOfChan); // avg. bytes/sec
    setUint16(numOfChan * 2);                      // block-align
    setUint16(16);                                 // 16-bit (hardcoded in this demo)

    setUint32(0x61746164);                         // "data" - chunk
    setUint32(length - pos - 4);                   // chunk length

    // write interleaved data
    for (i = 0; i < abuffer.numberOfChannels; i++)
        channels.push(abuffer.getChannelData(i));

    while (pos < length) {
        for (i = 0; i < numOfChan; i++) {             // interleave channels
            sample = Math.max(-1, Math.min(1, channels[i][offset])); // clamp
            sample = (0.5 + sample < 0 ? sample * 32768 : sample * 32767) | 0; // scale to 16-bit signed int
            view.setInt16(pos, sample, true);          // write 16-bit sample
            pos += 2;
        }
        offset++                                     // next source sample
    }

    // create Blob
    return new Blob([buffer], {type: "audio/wav"});

    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }

    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
}

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

const fromFile = () =>
    new Promise(resolve => {
        const audioBlob = fileInput.files[0];
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        const play = () => audio.play();

        resolve({audioBlob, audioUrl, play});

    });


const recordButton = document.querySelector('#record');
const fileButton = document.querySelector('#file')
const fileInput = document.querySelector('#file-input')
const stopButton = document.querySelector('#stop');
const playButton = document.querySelector('#play');
const sendButton = document.querySelector('#send');
const languageLabel = document.getElementById('language')
const filenameLabel = document.getElementById('filename')

let recorder;
let audio;

recordButton.addEventListener('click', async () => {
    recordButton.setAttribute('disabled', true);
    stopButton.removeAttribute('disabled');
    playButton.setAttribute('disabled', true);
    sendButton.setAttribute('disabled', true);
    fileButton.setAttribute('disabled', true);
    fileInput.value = null;
    filenameLabel.innerText = "None";
    if (!recorder) {
        recorder = await recordAudio();
    }
    recorder.start();
});

stopButton.addEventListener('click', async () => {
    startAnalyzeMode();
    audio = await recorder.stop();
});

function startAnalyzeMode() {
    recordButton.removeAttribute('disabled');
    stopButton.setAttribute('disabled', true);
    playButton.removeAttribute('disabled');
    playButton.removeAttribute('disabled');
    sendButton.removeAttribute('disabled');
    fileButton.removeAttribute('disabled');

}

sendButton.addEventListener('click', () => {
    let form_data = new FormData();
    languageLabel.innerText = 'Please wait...';
    if (!filenameLabel.innerText.localeCompare("None")) {
        let reader1 = new FileReader();
        reader1.onload = function (ev) {
            var audioCtx = new (AudioContext || webkitAudioContext)();
            // Decode audio
            audioCtx.decodeAudioData(ev.target.result).then(function (buffer) {
                // Process Audio
                var offlineAudioCtx = new OfflineAudioContext({
                    numberOfChannels: 2,
                    length: 44100 * buffer.duration,
                    sampleRate: 44100,
                });
                // Audio Buffer Source
                soundSource = offlineAudioCtx.createBufferSource();
                soundSource.buffer = buffer;
                compressor = offlineAudioCtx.createDynamicsCompressor();
                compressor.threshold.setValueAtTime(-20, offlineAudioCtx.currentTime);
                compressor.knee.setValueAtTime(30, offlineAudioCtx.currentTime);
                compressor.ratio.setValueAtTime(5, offlineAudioCtx.currentTime);
                compressor.attack.setValueAtTime(.05, offlineAudioCtx.currentTime);
                compressor.release.setValueAtTime(.25, offlineAudioCtx.currentTime);

                soundSource.connect(compressor);
                compressor.connect(offlineAudioCtx.destination);
                offlineAudioCtx.startRendering().then(function (renderedBuffer) {

                    blob = bufferToWave(renderedBuffer, offlineAudioCtx.length);
                    form_data.append('audio', blob, 'speech.wav');
                    fetch('/sound_analyze', {
                        method: 'POST',
                        body: form_data,
                        headers: {Accept: "application/json"}
                    }).then(
                        function (response) {
                            response.json().then(data => languageLabel.innerText = data.language)
                        });

                })
            });
        };
        reader1.readAsArrayBuffer(audio.audioBlob);
    } else {
        form_data.append('audio', audio.audioBlob, 'speech.wav');
        fetch('/sound_analyze', {
            method: 'POST',
            body: form_data,
            headers: {Accept: "application/json"}
        }).then(
            function (response) {
                response.json().then(data => languageLabel.innerText = data.language)
            });
    }

});

fileButton.addEventListener('click', () => fileInput.click())

fileInput.addEventListener('change', async () => {
    let pathParts = fileInput.value.split('\\');
    filenameLabel.innerText = pathParts[pathParts.length - 1];
    startAnalyzeMode();
    console.log(fileInput.files[0]);
    audio = await fromFile();
})

recordButton.removeAttribute('disabled');
stopButton.setAttribute('disabled', true);
playButton.setAttribute('disabled', true);
sendButton.setAttribute('disabled', true);


window.onload = function () {
    Visualizer.ini();
};

playButton.addEventListener('click', () => {
    audio.play();
    audio.audioBlob.arrayBuffer().then(arrayBuffer => Visualizer.audioContext.decodeAudioData(arrayBuffer, (audioBuffer) => {
        Visualizer._visualize(Visualizer.audioContext, audioBuffer);
    }))
});


let Visualizer = {
    ini: function () {
        this.source = null; //the audio source
        this.animationId = null;
        this.status = 0; //flag for sound is playing 1 or stopped 0
        this.forceStop = false;
        this._prepareAPI();
    },
    _prepareAPI: function () {
        window.AudioContext = window.AudioContext || window.webkitAudioContext || window.mozAudioContext || window.msAudioContext;
        window.requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame;
        window.cancelAnimationFrame = window.cancelAnimationFrame || window.webkitCancelAnimationFrame || window.mozCancelAnimationFrame || window.msCancelAnimationFrame;
        try {
            this.audioContext = new AudioContext();
        } catch (e) {
            console.log('!Your browser does not support AudioContext');
            console.log(e);
        }
    },
    _visualize: function (audioContext, buffer) {
        var audioBufferSouceNode = audioContext.createBufferSource(),
            analyser = audioContext.createAnalyser(),
            that = this;
        audioBufferSouceNode.connect(analyser);
        audioBufferSouceNode.buffer = buffer;
        if (!audioBufferSouceNode.start) {
            audioBufferSouceNode.start = audioBufferSouceNode.noteOn //in old browsers use noteOn method
            audioBufferSouceNode.stop = audioBufferSouceNode.noteOff //in old browsers use noteOff method
        }
        //stop the previous sound if any
        if (this.animationId !== null) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.source !== null) {
            this.source.stop(0);
        }
        audioBufferSouceNode.start(0);
        this.status = 1;
        this.source = audioBufferSouceNode;
        audioBufferSouceNode.onended = function () {
            that._audioEnd(that);
        };
        this._drawSpectrum(analyser);
    },
    _drawSpectrum: function (analyser) {
        var that = this,
            canvas = document.getElementById('canvas'),
            cwidth = canvas.width,
            cheight = canvas.height - 2,
            meterWidth = 10, //width of the meters in the spectrum
            capHeight = 2,
            capStyle = '#fff',
            meterNum = 800 / (10 + 2), //count of the meters
            capYPositionArray = []; ////store the vertical position of hte caps for the preivous frame
        ctx = canvas.getContext('2d');
        gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(1, '#0f0');
        gradient.addColorStop(0.5, '#ff0');
        gradient.addColorStop(0, '#f00');
        var drawMeter = function () {
            var array = new Uint8Array(analyser.frequencyBinCount);
            analyser.getByteFrequencyData(array);
            let allCapsReachBottom;
            if (that.status === 0) {
                //fix when some sounds end the value still not back to zero
                for (let i = array.length - 1; i >= 0; i--) {
                    array[i] = 0;
                }

                allCapsReachBottom = true;
                for (let i = capYPositionArray.length - 1; i >= 0; i--) {
                    allCapsReachBottom = allCapsReachBottom && (capYPositionArray[i] === 0);
                }

                if (allCapsReachBottom) {
                    cancelAnimationFrame(that.animationId); //since the sound is stoped and animation finished, stop the requestAnimation to prevent potential memory leak,THIS IS VERY IMPORTANT!
                    return;
                }

            }

            var step = Math.round(array.length / meterNum); //sample limited data from the total array
            ctx.clearRect(0, 0, cwidth, cheight);
            for (i = 0; i < meterNum; i++) {
                var value = array[i * step];
                if (capYPositionArray.length < Math.round(meterNum)) {
                    capYPositionArray.push(value);
                }

                ctx.fillStyle = capStyle;
                //draw the cap, with transition effect
                if (value < capYPositionArray[i]) {
                    ctx.fillRect(i * 12, cheight - (--capYPositionArray[i]), meterWidth, capHeight);
                } else {
                    ctx.fillRect(i * 12, cheight - value, meterWidth, capHeight);
                    capYPositionArray[i] = value;
                }

                ctx.fillStyle = gradient; //set the filllStyle to gradient for a better look
                ctx.fillRect(i * 12 /*meterWidth+gap*/, cheight - value + capHeight, meterWidth, cheight); //the meter
            }
            that.animationId = requestAnimationFrame(drawMeter);
        }
        this.animationId = requestAnimationFrame(drawMeter);
    },
    _audioEnd: function () {
        if (this.forceStop) {
            this.forceStop = false;
            this.status = 1;
            return;
        }
        this.status = 0;
    }
}
