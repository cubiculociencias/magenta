import tensorflow as tf
import numpy as np

class Model:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Configuración específica del modelo Onsets and Frames
        self.sample_rate = 16000
        self.hop_size = 512
        self.window_length = 2048
        
    def get_input_wav_length(self):
        return self.window_length
        
    def get_timestep(self):
        return self.hop_size * 1000 / self.sample_rate  # en ms
        
    def infer(self, audio):
        audio = np.array(audio, dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], audio)
        self.interpreter.invoke()
        return [
            self.interpreter.get_tensor(output['index'])
            for output in self.output_details
        ]
