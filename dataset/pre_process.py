# make CICIoT2023 dataset to instruction fine tuning dataset

import pandas as pd
import json


def make_instruction_fine_tuning_dataset(path_to_org_dataset: str, path_to_dst_dataset) -> bool:
    # read the original dataset
    df = pd.read_csv(path_to_org_dataset)
    
    json_data = []
    for index, row in df.iterrows():
        input_data = row.drop("label").to_dict()
        output_data = row["label"]
        
        json_data.append({
            "instruction": "Based on the network features, predict the type of traffic.",
            "input": input_data,
            "output": output_data
        })
        print(index)
    
    output_file = path_to_dst_dataset
    with open(output_file, 'w') as f:
        json.dump(json_data, f)

if __name__ == '__main__':
    make_instruction_fine_tuning_dataset("dataset/merge1.csv", "dataset/fine1.json")