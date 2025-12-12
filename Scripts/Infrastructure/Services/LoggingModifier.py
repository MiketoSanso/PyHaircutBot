import logging

from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder


class LoggingModifier:
    def __init__(self, path_finder: ProjectPathFinder):
        self.path_finder = path_finder
        self.configs_dir = self.path_finder.configs_path
        self.configs_dir.mkdir(exist_ok=True)
        self.root_logger = logging.getLogger()

        self.setup_logging()

    def setup_logging(self):
        self.root_logger.setLevel(logging.INFO)

        if self.root_logger.handlers:
            return

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        app_log_file = self.configs_dir / "app.log"
        app_handler = logging.FileHandler(app_log_file, encoding='utf-8')
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(formatter)
        self.root_logger.addHandler(app_handler)

        error_log_file = self.configs_dir / "errors.log"
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.root_logger.addHandler(error_handler)
