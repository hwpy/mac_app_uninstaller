from config import HOMEBREW_CASK_URL
from packages.api import BrewAPIHandler

handler = BrewAPIHandler()
files_to_remove = handler.get_files_to_remove(HOMEBREW_CASK_URL)
removed_data = handler.remove_data(files_to_remove)