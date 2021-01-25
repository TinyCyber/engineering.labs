### Prepare dataset
#### Description
This service ensures that the system has the required [dataset](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data?select=train.csv)
downloaded and preprocessed:
- The dataset is downloaded and tokenized into vectors of the same length, which is required for training.
- The embedding matrix and tokenizer are saved for future inference

#### Launching
Before running, make sure you've [added](./kaggle_creds/README.md) your Kaggle auth information.
There is a simple caching mechanism to skip costly (almost all) steps via
resulting files checksum verification.
Therefore, if you execute the code several times in a row, a real work will be performed only once,
and during all following launches these results will only be verified.

##### Docker-compose
1. Configure docker-engine to use at least 8GB+ of RAM and 1+ CPU.
2. `docker-compose build` - build docker image for data preparation.
3. `docker-compose run data_loader` - download and process data.
This step might take a while, depending on your network speed (~2.5 GB of data need to be downloaded) + embedding takes ~ 10-15 minutes.

As a result, the base dataset and the embedding file will be downloaded and saved into `dataset_storage` volume's root.
The preprocessed data will be saved into the `work_store` volume's root.

##### Local run (for debugging purposes)
1. Use Python 3.8+ and install needed requirements from [requirements.txt](./requirements.txt) with `pip isntall -r requirements.txt`
2. Being in the `data_loader` folder, execute the script: `python -u data_loader.py --dataset_name jigsaw-unintended-bias-in-toxicity-classification --storage_path dataset_storage --work_store_path work_store`.

It will download the base dataset and the embedding file into `dataset_storage` folder and save preprocessed data into the `work_store` directory.
An alternative way to configure the script: set the environment variables, which are defined for [data_loader](../docker-compose.yaml#L9) service in docker-compose.yaml file.
