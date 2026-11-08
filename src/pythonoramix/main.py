from pythonoramix.config import créer_application, créer_garde_manger
from pythonoramix.infrastructure.thermomix import Thermomix

application = créer_application(créer_garde_manger(), Thermomix())
