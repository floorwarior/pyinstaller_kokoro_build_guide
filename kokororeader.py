import os
import sys
import numpy as np
import traceback
import signal


if getattr(sys, 'frozen', False):
    # Running as compiled executable
    ISFROZEN = True
    BASE_PATH = sys._MEIPASS
    print(BASE_PATH)

    
else:
    # Running as normal Python script
    ISFROZEN = False
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    print(BASE_PATH)
    CURRENT_PYTHON = sys.executable


# block so pyinstaller finds the packages correctly:
# ------------------------------------------------
import numpy
import kokoro
import misaki
import spacy
import spacy.util
import spacy.cli
import torch
import soundfile
import sounddevice
#-------------------------------------------------



class KokoroReader():
    """takes the following arguments: 
    - models_folder: str or path
    - model: str or path
    - voice: str or path
    - config: str or path
    - gp2_model_folder : str or path
    before running this code, you will have to make some modifications: see README.md
    """

    def __init__(self, *args, **kwargs):
        try:
            import soundfile as sf
            from kokoro import KPipeline,KModel
            import sounddevice as sd
      
            self.sf = sf
            self.sd = sd
            self.models_folder = kwargs.get("models_folder")
            self.base_path = kwargs.get("base_path")
            self._model = kwargs.get("model") # .pth relative path to the folder
            self._voice = kwargs.get("voice") # .pt relative path to the folder
            self._config = kwargs.get("config") # config.json relative path to the folder
            self._gp2_model_folder = kwargs.get("gp2_model_folder") 
            self.pipeline = KPipeline(
                gp2_model_path=os.path.join(self.base_path,self._gp2_model_folder),
                lang_code=kwargs.get("lang_code"),
                model=KModel(
                    model=os.path.join(self.base_path,self.models_folder,self._model),
                    config=os.path.join(self.base_path,self.models_folder,self._config)
                    )
                )
            self.imported_ok = True
            self.ready = True
        except Exception as e:
            traceback.print_exc()
            self.imported_ok = False
            self.error = e


   
    def save_audio(self,*args,**kwargs):
        text = kwargs.get("text")
        audio_out_name = kwargs.get("filename")
        generator = self.pipeline(text,voice=os.path.join(self.base_path,self.models_folder,self._voice))

        parts = []
        for i, (gs, ps, audio) in enumerate(generator):
            #print(i, gs, ps)
            #display(Audio(data=audio, rate=24000, autoplay=i==0))
            parts.append(audio)
            #sf.write(f'{i}.wav', audio, 24000)
        added = np.concatenate(parts)
        self.sf.write(audio_out_name,added,24000)

    def Speak(self,*args,**kwargs):
        text = kwargs.get("text")
        generator = self.pipeline(text,voice=os.path.join(self.base_path,self.models_folder,self._voice))

        parts = []
        for i, (gs, ps, audio) in enumerate(generator):
            #print(i, gs, ps)
            #display(Audio(data=audio, rate=24000, autoplay=i==0))
            parts.append(audio)
            self.sd.play(audio, 24000)
            self.sd.wait()


if __name__ == "__main__":
    def exit():
        pid = os.getpid()
        os.kill(pid,signal.SIGINT)

    reader = KokoroReader(
        base_path = BASE_PATH, # folder where pyinstaller is running: _internal in most cases
        lang_code = "a",
        models_folder="kokoromodels",
        voice="af_heart.pt", # notice that this is a filename
        model = "kokoro-v1_0.pth",
        config = "config.json",
        gp2_model_folder = "en_core_web_sm/en_core_web_sm-3.8.0" # <- copy this folder to . from .venv/Lib/site-packages/en_core_web_sm NOTE: this might be different for you, but it should be the same concept
        )
    while True:
        text = input("text:")
        if text.lower() == "q":
            exit()
        filename = input("filename: ( leave empty if you only want to listen )")

        if filename.endswith(".wav"):
            reader.save_audio(text=text,filename=filename)
        else:
            reader.Speak(text=text)
    # this implementation is for english only, you might find other errors when using other models,
