from app import app
from pyfladesk import init_gui




if __name__ == '__main__':
    init_gui(app.server, window_title='Desktop App')