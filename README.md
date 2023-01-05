# pulseapi-python-clinicaltrials

This python code gives a clear example of how to use the Pluto API to pull all Clinical Trial information from the API and write the Trial Detail data into a file as well as the Clinical Trial Eligibility data into a file so that you can see the API operating and ensure that your own API oAuth credentials work. 

It calls the following Pluto API.
* Call the Clinical Trials API
```
/clinical-trials
```

* Call the API which retrieves detailed clinical trial information
```
/clinical-trials/{study-id}
```

* Call the clinical trial eligible API
```
/clinical-trials/{study-id}/eligible
```

# Configure your environment

Here are some important environment variables you need to configure before run the code.
```
CLIENT_ID = <INSERT YOUR CLIENT ID HERE>
CLIENT_SECRET = <INSERT YOUR CLIENT SECRET HERE>
```
Please replace those two placeholders with your own credentials.

```
LOGS_FILE_PATH = "clinical_trials_logs"
DATA_FILE_PATH = "clinical_trials_data_files"
```
You can change the folder to where to store the logs and data files of patients.

# Run the code
Python 3.10.6 is used for this repository.\
You can run the code with the following command.
```
python3.10 request.py
```
