import getpass
import json
import logging
import os
from pprint import pformat
from shutil import rmtree
from urllib import request


class BrewAPIHandler:
    """Homebrew API handler for casks"""

    APP_FOLDER = "/Applications/"
    USER_FOLDER = "/Users/" + getpass.getuser()

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("uninstall_by_brew")

    def get_files_to_remove(self, url: str) -> list[str]:
        """Generate paths to files to remove

        Arguments:
            - url (str) - URL for getting info from Homebrew API

        Returns:
            list[str] - list of files and dirs to remove
        """
        to_remove: list[str] = []
        with request.urlopen(url) as response:
            data = json.load(response)
            self.logger.debug(pformat(data))
            try:
                to_remove += [self.APP_FOLDER + data.get("artifacts")[0].get("app")[0]]
            except Exception as _:
                self.logger.warning("app not found in json!")
            try:
                to_remove += data.get("artifacts")[1].get("zap")[0].get("rmdir")
            except Exception as _:
                self.logger.warning("rmdir not found in json!")
            try:
                to_remove += data.get("artifacts")[1].get("zap")[0].get("trash")
            except Exception as _:
                self.logger.warning("trash not found in json!")

        to_remove = list(map(lambda x: x.replace("~", self.USER_FOLDER), to_remove))
        return to_remove

    def remove_data(self, to_remove: list[str]) -> list[str]:
        """Remove data by to_remove list

        Arguments:
            - to_remove (list[str]) - list of files and dirs to remove

        Returns:
            list[str] - deleted files and dirs

        Exceptions:
            - ValueError: A string was expected, got {type(agreement)}!
        """
        deleted: list[str] = []
        self.logger.warning(
            f"The following packages will be deleted: \n{pformat(to_remove)}\n"
        )
        agreement = input("[Y/n]: ")
        if not isinstance(agreement, str):
            raise ValueError(f"A string was expected, got {type(agreement)}!")
        else:
            agreement = agreement[0].lower()
            if agreement == "n":
                self.logger.info("Canceled.")
            elif agreement == "y":
                for item in to_remove:
                    try:
                        to_del = os.path.abspath(item)
                        rmtree(to_del)
                        self.logger.info(f"\nDeleted: {to_del}.\n")
                        deleted.append(to_del)
                    except Exception as ex:
                        self.logger.exception(ex)
                        continue
            else:
                self.logger.exception("Unexpected.")
        return deleted
