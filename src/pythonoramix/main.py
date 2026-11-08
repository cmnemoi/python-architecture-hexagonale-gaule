from pythonoramix.config import créer_l_application, créer_le_garde_manger
from pythonoramix.infrastructure.thermomix import Thermomix

application = créer_l_application(créer_le_garde_manger(), Thermomix())
