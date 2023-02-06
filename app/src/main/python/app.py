import torch
import commons
import utils
from text import text_to_sequence
from os.path import dirname, join
from scipy.io import wavfile
from models import SynthesizerTrn
from text.symbols import symbols
import io

filename = join(dirname(__file__), "model/config.json")
hps = utils.get_hparams_from_file(filename)

model = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
model.eval()
model.load_state_dict(torch.load(join(dirname(__file__), "model/chinese.pth")))

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    print(text_norm)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def vc_fn(input):
    stn_tst = get_text(input, hps)
    with torch.no_grad():
        x_tst = stn_tst.unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
        audio = model.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
    samplerate = hps.data.sampling_rate
    f = io.BytesIO()
    wavfile.write(f,samplerate,audio)
    return f.getvalue()
