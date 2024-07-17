CASK = input("Input app name as cask named on https://formulae.brew.sh/: ")
HOMEBREW_API_URL: str = "https://formulae.brew.sh/api/cask.json"
HOMEBREW_CASK_URL: str = f"https://formulae.brew.sh/api/cask/{CASK}.json"
