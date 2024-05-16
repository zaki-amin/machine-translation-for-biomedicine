import os

from datasets import DatasetDict, load_dataset, concatenate_datasets


def load_corpus(data_filename: str, validation_proportion: float, seed: int) -> DatasetDict:
    """Reads a JSONL file for a parallel corpus into a DatasetDict for fine-tuning
    :param data_filename: path to the JSONL file containing the parallel corpus
    :param validation_proportion: the proportion of the data to use for validation
    :param seed: the random seed to use for splitting the data"""
    training_data = load_dataset("json", data_files=data_filename)
    train_proportion = 1 - validation_proportion
    split_datasets = training_data["train"].train_test_split(train_size=train_proportion, seed=seed)
    split_datasets["validation"] = split_datasets.pop("test")
    return split_datasets


def get_all_filepaths(directory_path: str) -> list[str]:
    """Gets all filepaths in a directory"""
    return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path)]


def load_all_corpora(directory_path: str, validation_proportion: float, seed: int) -> DatasetDict:
    """Loads all corpora in a directory and concatenates them into a single DatasetDict"""
    concatenated_datasets = {}
    for filepath in get_all_filepaths(directory_path):
        corpus = load_corpus(filepath, validation_proportion, seed)
        # Concatenate each key separately
        for split in corpus.keys():
            if split not in concatenated_datasets:
                concatenated_datasets[split] = corpus[split]
            else:
                concatenated_datasets[split] = concatenate_datasets([concatenated_datasets[split], corpus[split]])

    return DatasetDict(concatenated_datasets)
