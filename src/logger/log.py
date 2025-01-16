import logging.config
import json

config = r"D:\sparta-utils-project\playwright-rolex\config\logging_config.json"
with open(config, 'r') as f:
    log_config = json.load(f)
    logging.config.dictConfig(log_config)

scrape_logger = logging.getLogger()


def main():
    pass


if __name__ == '__main__':
    main()
