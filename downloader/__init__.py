import logging
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.absolute()
filename= root_path / "log.log"
logging.basicConfig(filename= filename, filemode = 'a', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
