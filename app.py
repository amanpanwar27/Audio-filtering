from flask import Flask, request, send_file, render_template
import librosa
import numpy as np
import soundfile as sf
print(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    # Access the uploaded audio file from the request
    audio_file = request.files['audio']
    # Save the audio file locally
    audio_path = 'uploaded_audio.wav'
    audio_file.save(audio_path)

    # Perform the audio filtering
    y, sr = librosa.load(audio_path)

    # Define frequency ranges to select
    fmin1 = 35  # minimum frequency for range 1
    fmax1 = 95  # maximum frequency for range 1

    args = request.args
    animal = args.get("value")
    if(animal == 0):
        fmin1 = 35  # minimum frequency for range 1
        fmax1 = 95  # maximum frequency for range 1
    else :
        fmin1 = 60
        fmax1 = 160
    # Get spectrogram of audio signal
    D = np.abs(librosa.stft(y))

    # Define frequency bin indices for the range
    freq_bins = librosa.fft_frequencies(sr=sr, n_fft=len(D))
    idx1 = np.where((freq_bins >= fmin1) & (freq_bins <= fmax1))[0]

    # Create a mask to select the frequency range
    mask = np.zeros(D.shape)
    mask[idx1, :] = 1

    # Apply the mask to the spectrogram
    D_masked = D * mask

    # Reconstruct audio signal from masked spectrogram
    y_reconstructed = librosa.istft(D_masked)

    # Save the filtered audio
    output_path = 'filtered_audio.wav'
    sf.write(output_path, y_reconstructed, sr)

    # Return the filtered audio file to the client
    return send_file(output_path, as_attachment=True)

if __name__== '__main__':
    app.run(debug=True)