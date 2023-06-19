const processAudio = ()=> {
            var fileInput = document.getElementById("audio-upload");
            var file = fileInput.files[0];

            var formData = new FormData();
            formData.append("audio", file);
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/process-audio", true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    
                    // var audioPlayer = document.getElementById("audio-player");
                    let url =  URL.createObjectURL(xhr.response);
                    // audioPlayer.load();
                    const wavesurfer = WaveSurfer.create({
                    container: document.body,
                    waveColor: 'rgb(200, 0, 200)',                     
                    progressColor: 'rgb(100, 0, 100)',
                    url: url,
                })
                    wavesurfer.once('interaction', () => {
                        wavesurfer.play()
                    })
                    // document.getElementById("output-audio").style.display = "block";
                }
            };
            xhr.responseType = "blob";
            xhr.send(formData);
}
