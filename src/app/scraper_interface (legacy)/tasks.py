import subprocess

from celery import Celery

try:
    from app.config import settings
except ModuleNotFoundError:
    from config import settings


app = Celery(
    "scraper_tasks",
    broker=settings.rabbitmq_broker_url,
    backend=settings.redis_backend_url,
)


def generate_spider_params_string(params: dict) -> str:
    """Generates param string that can be passed to -a argument of scrapy crawl

    Args:
        params (dict): parameters

    Returns:
        str: parameter string
    """

    parameters = ""
    for key, value in params.items():
        value = str(value)
        # Check if spaces are present in value
        if value.find(" ") == -1:
            parameters += f"{key}={str(value)} "
        else:
            parameters += f"{key}='{str(value)}' "

    return parameters


@app.task
def start_spider(spider_name: str, params: dict=None):
    """
    Run spider seperate from main proccess
    """

    # Generate command
    if params:
        parameter_string = generate_spider_params_string(params)
        code = subprocess.call(
            ["./scraper_interface/run_spider.sh", spider_name, parameter_string],
        )
    else:
        code = subprocess.call(
            ["./scraper_interface/run_spider.sh", spider_name],
        )
    
    print(code)
    return code
