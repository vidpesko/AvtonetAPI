from datetime import datetime

# Scraper intput validations
SCRAPER_ALLOWED_SCHEMES = ["https", ]
SCRAPER_ALLOWED_DOMAINS = ["www.avto.net", "avto.net"]


# Maximum Vehicle entry age - maximum amount of time before Vehicle needs updating
MAX_VEHICLE_AGE = 15  # In minutes