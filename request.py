import requests
import json
import os
import base64
from constants import *


# write log data into a log file
# log_str_arr is an array of log string
def writeLog(log_arr):

    if not os.path.exists(LOGS_FILE_PATH):
        os.makedirs(LOGS_FILE_PATH)
    logs_file = os.path.join(LOGS_FILE_PATH, "clinical-trials-api-logs.dat")
    with open(logs_file, "w") as outfile:
        outfile.write('\n'.join(log_arr))


# main function
def main():

    log_str_arr = []

    auth_header = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode()).decode()
    payload = {"grant_type": "client_credentials", "client_id": CLIENT_ID}
    headers = {'Authorization': "Basic " + auth_header,
               'Content-Type': 'application/x-www-form-urlencoded'
               }

    response = requests.request(
        "POST", OAUTH_ENDPOINT, headers=headers, data=payload)
    # stop if we fail to get access code
    if response.status_code != 200:
        log_str_arr.append(STR_CRED_INCORRECT)
        writeLog(log_str_arr)
        return

    access_token = response.json()['access_token']

    # Feel free to change the start and length here
    query = {'length': 2, 'start': 1}
    headers = {"Authorization": "Bearer " + access_token}
    clinicaltrials_endpoint = BASE_URL + "/clinical-trials"
    response = requests.get(
        clinicaltrials_endpoint, headers=headers, params=query)

    print("Status Code", response.status_code)

    # Stop in case oAuth credential is incorrect
    if response.status_code == 401:  # Unauthorized
        log_str_arr.append(STR_CRED_INCORRECT)
        writeLog(log_str_arr)
        return

    clinical_trials = response.json()['content']['data']
    # Stop in case there are no clinical trials in the organization
    if len(clinical_trials) == 0:
        log_str_arr.append(STR_NO_CLINICAL_TRIALS)
        writeLog(log_str_arr)
        return

        # Otherwise, we are good to move on
    log_str_arr.append(clinicaltrials_endpoint)

    for clinical_tiral in clinical_trials:
        clinical_tiral_id = clinical_tiral['study_id']

        ##
        # for each clinical trial call client trial detail API
        ##
        clinical_tiral_detail_endpoint = BASE_URL + \
            "/clinical-trials/" + clinical_tiral_id

        response = requests.get(
            clinical_tiral_detail_endpoint, headers=headers)

        # Stop in case we meet error calling clinical trial detail api
        if response.status_code != 200:
            log_str_arr.append(STR_SERVER_ERROR)
            writeLog(log_str_arr)
            return

        log_str_arr.append(clinical_tiral_detail_endpoint)

        # Writing to data file
        if not os.path.exists(DATA_FILE_PATH):
            os.makedirs(DATA_FILE_PATH)
        data_file = os.path.join(
            DATA_FILE_PATH, "clinical-trial-" + clinical_tiral_id + ".json")
        with open(data_file, "w") as outfile:
            outfile.write(json.dumps(response.json()))

        ##
        # for each clinical trial call client trial eligible API
        ##
        clinical_tiral_elgible_endpoint = BASE_URL + \
            "/clinical-trials/" + clinical_tiral_id + "/eligible"

        response = requests.get(
            clinical_tiral_elgible_endpoint, headers=headers)

        # Stop in case we meet error calling clinical trial eligible api
        if response.status_code == 204:
            log_str_arr.append(STR_NO_CONTENT)
            writeLog(log_str_arr)
            return

        if response.status_code != 200:
            log_str_arr.append(STR_SERVER_ERROR)
            writeLog(log_str_arr)
            return

        log_str_arr.append(clinical_tiral_elgible_endpoint)

        # Writing to data file
        if not os.path.exists(DATA_FILE_PATH):
            os.makedirs(DATA_FILE_PATH)
        data_file = os.path.join(
            DATA_FILE_PATH, "clinical-trial-eligible-" + clinical_tiral_id + ".json")
        with open(data_file, "w") as outfile:
            outfile.write(json.dumps(response.json()))

        # Writing to log file
    writeLog(log_str_arr)
    print("successfully printed data and log")
    return


if __name__ == "__main__":
    main()
