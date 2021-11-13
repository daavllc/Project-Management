import logging

class Logger:
    def __new__(cls, name: str):
        """Generates logging.logger with defaults set

        Args:
            name (str): specify the logger's name

        Returns:
            logging.logger
        """
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

        sh = logging.StreamHandler()
        fh = logging.FileHandler(filename="gui.log")
        sh.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        log.addHandler(sh)
        log.addHandler(fh)
        return log