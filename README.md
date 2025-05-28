# prog-lab6
По-сути готовый проект, все задание готово к проверке.
Необходимо только сбилдить через docker-compose run web alembic init alembic
И добавить в создавшийся alembic/env.py
from models import Base
target_metadata = Base.metadata
