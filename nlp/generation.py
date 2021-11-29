from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

def train_model(file, output_dir):
    train_tokenizer(file)
    tokenizer_file = "aitextgen.tokenizer.json"
    config = GPT2ConfigCPU()
    ai = aitextgen(tokenizer_file=tokenizer_file, config=config)
    data = TokenDataset(file, tokenizer_file=tokenizer_file, block_size=64)
    ai.train(data, batch_size=8, num_steps=50000, \
        generate_every=5000, save_every=5000, output_dir=output_dir)
    ai.save(target_folder=output_dir)
    return ai

if __name__ == "__main__":
    # train_model('../data/data/QC/merged-CLEAN.txt', 'models/QC')
    train_model('../data/data/CA/merged-CLEAN.txt', 'models/CA')