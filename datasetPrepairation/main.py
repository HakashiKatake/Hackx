from datasets import load_dataset


dataset = load_dataset("csv", data_files="./datasetPrepairation/rawDatasets/bdm.csv")


# map over the dataset and replace the ShoulderWidth in inches to centimeters
def convert_to_cm(example):
    example["ShoulderWidth"] = example["ShoulderWidth"] * 2.54
    example["ChestWidth"] = example["ChestWidth"] * 2.54
    example["Belly"] = example["Belly"] * 2.54
    example["Waist"] = example["Waist"] * 2.54
    example["Hips"] = example["Hips"] * 2.54
    example["ArmLength"] = example["ArmLength"] * 2.54
    example["WaistToKnee"] = example["WaistToKnee"] * 2.54
    example["ShoulderToWaist"] = example["ShoulderToWaist"] * 2.54
    example["LegLength"] = example["LegLength"] * 2.54
    example["TotalHeight"] = example["TotalHeight"] * 2.54
    return example


dataset = dataset.map(convert_to_cm)

print(dataset)

# save the dataset
