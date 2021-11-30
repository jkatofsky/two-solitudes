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
    # train_model('../data/data/CA/merged-CLEAN.txt', 'models/CA')
    QC_model = aitextgen(model_folder='models/QC', \
        tokenizer_file='models/QC/aitextgen.tokenizer.json')
    CA_model = aitextgen(model_folder='models/CA', \
        tokenizer_file='models/CA/aitextgen.tokenizer.json')
    prompts = ['quebec is', 'canada is']
    # QC_model.generate_to_file(n=100, destination_path='models/QC/samples.txt')
    # CA_model.generate_to_file(n=100, destination_path='models/CA/samples.txt')
    for prompt in prompts:
        print('QUEBEC:')
        QC_model.generate(n=20, prompt=prompt)
        print('CANADA:')
        QC_model.generate(n=20, prompt=prompt)
    # print(QC_outputs)
    # print(CA_outputs)