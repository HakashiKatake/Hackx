from datasets import load_dataset

import pandas as pd

dataset = load_dataset(
    "csv", data_files="./datasetPrepairation/rawDatasets/bdm.csv", split="train"
)


# map over the dataset and replace the ShoulderWidth in inches to centimeters
def convert_to_cm(example):
    #  limit to 2 deciaml places

    example["ShoulderWidth"] = round(example["ShoulderWidth"] * 2.54, 2)
    example["ChestWidth"] = round(example["ChestWidth"] * 2.54, 2)
    example["Belly"] = round(example["Belly"] * 2.54, 2)
    example["Waist"] = round(example["Waist"] * 2.54, 2)
    example["Hips"] = round(example["Hips"] * 2.54, 2)
    example["ArmLength"] = round(example["ArmLength"] * 2.54, 2)
    example["WaistToKnee"] = round(example["WaistToKnee"] * 2.54, 2)
    example["ShoulderToWaist"] = round(example["ShoulderToWaist"] * 2.54, 2)
    example["LegLength"] = round(example["LegLength"] * 2.54, 2)
    example["HeadCircumference"] = round(example["HeadCircumference"] * 2.54, 2)
    example["TotalHeight"] = round(example["TotalHeight"] * 2.54, 2)
    return example


dataset = dataset.map(convert_to_cm)

# convert dataset to pandas dataframe
dataset = pd.DataFrame(dataset)
# save it on disk as csv
dataset.to_csv("./datasetPrepairation/processedDatasets/bdm.csv", index=False)

print(dataset)

# save the dataset
