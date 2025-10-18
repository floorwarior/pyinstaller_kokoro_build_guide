# Kokoro can be a bit tricky when it comes to pyinstaller
it includes dinnamic downloads which run in a subprocess, the problem?
it grabs sys.executable which is your_apps.exe, this in turn will create an endless call loop
and you package will never be download.
## Steps to make it work:
1. open the normal_kokoro.py file, set the voice you want, run the normal_kokoro file **once**
2. once it runs, navigate here ( or similar) c:/Users/yourusername/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/somerandomstring/
open it, there is going to be:
- config.json | copy this into the kokoromodels folder
- kokoro-v1_0.pth | and this
- /voices folder | copy the desired voice from this folder into the kokoromodels folder 
3. Lib modifications:
navigate here first:
.venv/Lib/site-packages/misaki/en/
find the G2P class , modify it like so:

    ```
    class G2P:
        def __init__(self, model_path=None,version=None, trf=False, british=False, fallback=None, unk='❓'): # <- we have added the model_path
            self.version = version
            self.british = british
            # name = f"en_core_web_{'trf' if trf else 'sm'}"
            # if not spacy.util.is_package(name):
            #    spacy.cli.download(name) # this is the download that will break your exe, if it runs
            components = ['transformer' if trf else 'tok2vec', 'tagger']
            self.nlp = spacy.load(model_path, enable=components) # <- used here
            self.lexicon = Lexicon(british)
            self.fallback = fallback if fallback else None
            self.unk = unk
    ```

    next navigate to this file:
    .venv/Lib/site-packages/kokoro/pipeline.py
    modify the initializer to accept that path, which we gonna pass to G2P:

    ```

        def __init__(
        self,
        lang_code: str,
        gp2_model_path = None, # <- add this line
        repo_id: Optional[str] = None,
        model: Union[KModel, bool] = True,
        trf: bool = False,
        en_callable: Optional[Callable[[str], str]] = None,
        device: Optional[str] = None
    ):
    # . . . 
    self.g2p_model_path = g2p_model_path # <- wherever G2P is called pass this value to GP2 as model_path
    then:

    ...
    if lang_code in 'ab':
        try:
            fallback = espeak.EspeakFallback(british=lang_code=='b')
        except Exception as e:
            logger.warning("EspeakFallback not Enabled: OOD words will be skipped")
            logger.warning({str(e)})
            fallback = None
        self.g2p = en.G2P(trf=trf,model_path = self.g2p_model_path, british=lang_code=='b', fallback=fallback, unk='')
    ...

    ```
    find this folder: .venv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.8.0
    copy en_core_web_sm to the root of the project.
    i searched around in the code a bit, as far as i can tell there should be no other dinamic downloads

    if all of this is done run the kokororeader file, if it works ( which it should ), build the project with
    
    ```pyinstaller kokororeader.spec```

    the spec file pulls data / folders which are imperative for this to work
