from transformers import Wav2Vec2ForCTC, Wav2Vec2CTCTokenizer, Wav2Vec2Processor
import torch
import librosa 
import torchaudio


model_path = "/home/pi/Desktop/asr-model/saved_model"

asr_model = Wav2Vec2ForCTC.from_pretrained(model_path)
tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(model_path)
asr_processor = Wav2Vec2Processor.from_pretrained(model_path)

def transcribe_audio(audio_file_path):

    waveform, rate = librosa.load(audio_file_path, sr=16000, mono=True)
    
    # Process mel spectrogram for ASR model
    inputs = asr_processor(waveform, return_tensors='pt', padding=True, sampling_rate=16000)

    # Run through ASR model
    with torch.no_grad():
        logits = asr_model(**inputs).logits
    
    # Get predicted ids and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = asr_processor.batch_decode(predicted_ids)

    return transcription

