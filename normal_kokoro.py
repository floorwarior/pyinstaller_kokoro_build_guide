
# 3️⃣ Initalize a pipeline
from kokoro import KPipeline
import soundfile as sf
import torch

pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice, reference above.


text = '''
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
'''

generator = pipeline(
    text, voice='af_heart', # <= change voice here
    speed=1, split_pattern=r'\n+'
)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f'{i}.wav', audio, 24000) # save each audio file