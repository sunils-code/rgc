import os
import yaml

def load_config():
    # load yaml
    # directory of file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.yaml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # get project root
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    # create full paths
    data_dir = os.path.join(project_root, config["data_dir"])
    db_file = os.path.join(project_root, config["db_file"])

    companies_file = os.path.join(data_dir, config["files"]["companies"])
    people_folder = os.path.join(data_dir, config["files"]["people_folder"])
    market_folder = os.path.join(data_dir, config["files"]["market_data_folder"])
    financial_statement_folder = os.path.join(data_dir, config["files"]["financial_statement_folder"])

    # format the SQLite URI using the path
    sqlite_uri = config["database"]["sqlite_uri_template"].format(db_file=db_file)

    return {
        "BASE_DIR": project_root,
        "DATA_DIR": data_dir,
        "DB_FILE": db_file,
        "COMPANIES_FILE": companies_file,
        "SQLITE_URI": sqlite_uri,
        "PEOPLE_FOLDER": people_folder,
        "MARKET_DATA_FOLDER": market_folder,
        "FINANCIAL_STATEMENT_FOLDER": financial_statement_folder
    }

# load config
config = load_config()
