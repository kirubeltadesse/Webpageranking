from django.apps import AppConfig

from bokeh.server.server import Server

import signal
from tornado.ioloop import IOLoop

from . import bk_sliders
from . import bk_config

def on_shutdown():
    print('Shutting down')
    IOLoop.instance().stop()


def bk_worker():
    # Note: num_procs must be 1
    server = Server({'/bk_sliders_hist':bk_sliders.histogram_tab,'/bk_sliders_bar':bk_sliders.barrank_tab,
    '/bk_sliders_den':bk_sliders.density_tab,'/bk_sliders_tab':bk_sliders.table_tab},
                    io_loop=IOLoop(),
                    address=bk_config.server['address'],
                    port=bk_config.server['port'],
                    allow_websocket_origin=["localhost:8000"]
                    )
    print("starting server")
    server.start()
    # server.io_loop.instance()
    server.io_loop.start()


class BokehAppConfig(AppConfig):
    name = 'bokeh_app'
    def ready(self):
        from threading import Thread
        Thread(target=bk_worker).start()
