# app-versions-dashboard 

Uses python 3

## Run locally :

```
# python3 -m venv

# source venv/bin/activate

# pip install -r requirements.txt

# python buildVersionDashboard.py -h 

usage: buildVersionDashboard.py [-h] -g GROUP_VAR_FOLDER
                                [-f GROUP_VAR_FILE_PREFIX]
                                [-s SERVERLESS_VAR_FILE_PREFIX] [--force]
                                [-e EXPORTED_FILE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP_VAR_FOLDER, --group-var-folder GROUP_VAR_FOLDER
                        Group Var folder
  -f GROUP_VAR_FILE_PREFIX, --group-var-file-prefix GROUP_VAR_FILE_PREFIX
                        Group Var env file prefix
  -s SERVERLESS_VAR_FILE_PREFIX, --serverless-var-file-prefix SERVERLESS_VAR_FILE_PREFIX
                        Serverless Var env file prefix
  --force               Do not ask confirmations
  -e EXPORTED_FILE_PATH, --exported-file-path EXPORTED_FILE_PATH
                        Path where to export the html file
```                        
