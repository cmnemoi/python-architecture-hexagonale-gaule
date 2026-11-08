from pythonoramix.config import créer_l_application, créer_le_garde_manger
from pythonoramix.infrastructure.thermomix_en_memoire import ThermomixEnMémoire

application = créer_l_application(créer_le_garde_manger(), ThermomixEnMémoire())
