import os

def get_data(QC_or_CA, exclude=[]):
    print(f"Getting data for {QC_or_CA} without {exclude}...")
    data = []
    base = f'../data/data/{QC_or_CA}'
    for filename in [filename for filename in os.listdir(base) if 'CLEAN' in filename]:
        if any(filename.startswith(sr) for sr in exclude):
            continue
        with open(f'{base}/{filename}') as fp:
            data.extend(fp.readlines())
    print(f"Returning {len(data)} comments")
    return data