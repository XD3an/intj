import pandas as pd
import json
import random

def ciciot2023_to_ift(path_to_org_dataset: str, path_to_dst_dataset, line: int) -> bool:
    df = pd.read_csv(path_to_org_dataset)
    
    instruction_list = [
        "Based on the network features, predict the type of traffic.",
        "Analyze the following network features during an unexpected spike in traffic and classify the traffic type.",
        "Given the network features, predict the type of traffic.",
        "Based on the network features, classify the traffic type.",
        "Given the network features, classify the traffic type.",
        "Analyze the network features and classify the traffic type.",
        "Given the network features, predict the type of traffic.",
        "Analyze the network features and predict the type of traffic.",
        "Given the network features, classify the traffic type.",
        "Analyze the network features and classify the traffic type.",
    ]
    
    json_data = []
    times = 0
    for index, row in df.iterrows():
        times += 1
        input_data = row.drop("label").to_dict()
        output_data = row["label"]
        
        json_data.append({
            "instruction": random.choice(instruction_list),  
            "input":  f"{input_data}",
            "output": output_data
        })
        print(index)
        if times == (line+1):
            break
    
    output_file = path_to_dst_dataset
    with open(output_file, 'w') as f:
        json.dump(json_data, f)

if __name__ == '__main__':
    ciciot2023_to_ift("dataset/CICIoT2023_merge1.csv", "dataset/CICIoT2023_ift1_100.json", 100)