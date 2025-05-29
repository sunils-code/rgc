import os
import yaml

def load_config():
    # load yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # get base directory of file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    #print(base_dir)

    # create full paths
    data_dir = os.path.join(base_dir, config["data_dir"])
    db_file = os.path.join(base_dir, config["db_file"])

    companies_file = os.path.join(data_dir, config["files"]["companies"])
    people_folder = os.path.join(data_dir, config["files"]["people_folder"])
    

    # format the SQLite URI using the path
    sqlite_uri = config["database"]["sqlite_uri_template"].format(db_file=db_file)

    return {
        "BASE_DIR": base_dir,
        "DATA_DIR": data_dir,
        "DB_FILE": db_file,
        "COMPANIES_FILE": companies_file,
        "SQLITE_URI": sqlite_uri,
        "PEOPLE_FOLDER": people_folder
    }

# load config
config = load_config()
