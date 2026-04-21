import torch
import json
from model import DeepLogModel

class DeepLogInference:
    def __init__(self, model_path, mapping_path, window_size=10, top_k=9):
        self.window_size = window_size
        self.top_k = top_k

        with open(mapping_path) as f:
            self.event2idx = json.load(f)

        self.unk = self.event2idx["UNK"]

        self.model = DeepLogModel(len(self.event2idx))
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()

        self.windows = {}

    def process_event(self, block_id, event):
        idx = self.event2idx.get(event, self.unk)

        if block_id not in self.windows:
            self.windows[block_id] = []

        self.windows[block_id].append(idx)

        if len(self.windows[block_id]) < self.window_size + 1:
            return None

        seq = self.windows[block_id][-(self.window_size + 1):]

        x = torch.tensor([seq[:-1]])

        with torch.no_grad():
            out = self.model(x)
            topk = torch.topk(out, self.top_k, dim=1).indices[0].numpy()

        target = seq[-1]

        return 0 if target in topk else 1