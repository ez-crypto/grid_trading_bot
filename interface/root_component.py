# Root
# Display the interface

from tkinter import *
import datetime
from interface.styling import *
from strategy import GridTrading
from connectors.api import BinanceTestnetApi
from connectors.websocket import BinanceTestnetWebsocket
from interface.messages_component import Messages
from interface.strategy_component import StrategyFrame
from interface.orders_component import OrdersFrame
from models import *
from interface.styling import *
import logging

logger = logging.getLogger()

class Root(Tk):
    def __init__(self, strategy: GridTrading, api: BinanceTestnetApi, websocket: BinanceTestnetWebsocket):
        super().__init__()
        self.title("Grid Trading")
        self._strategy = strategy
        self._api = api
        self._websocket = websocket
        # Divide the window in 2 frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._left_frame = Frame(self, bg=BG_COLOR)
        self._left_frame.grid(row=0, column=0, sticky=N+S+W+E)
        self._right_frame = Frame(self, bg=BG_COLOR)
        self._right_frame.grid(row=0, column=1, sticky=N+S+W+E)
        # Frames
        self._messages_frame = Messages(self._right_frame)
        self._messages_frame.grid(row=0, column=0, sticky=N+S+W+E)
        self._open_orders_frame = OrdersFrame([{'label': 'Time', 'name': 'order_time', 'func':lambda t:datetime.datetime.fromtimestamp(int(t/1e3)).strftime('%d-%m-%Y %H:%M:%S') }, {'label': 'Price', 'name': 'price', 'func': lambda x:str(x)}, {'label': 'Side', 'name': 'side', 'func': lambda x:str(x)}, {'label': 'Quantity', 'name': 'quantity', 'func': lambda x:str(x)}], "Open Orders", self._right_frame)
        self._open_orders_frame.grid(row=1, column=0, sticky=N+S+W+E)
        self._strategy_frame = StrategyFrame(self._strategy, self._messages_frame, self._left_frame)
        self._strategy_frame.grid(row=0, column=0, sticky=N+S+W+E)
        # Initialising update
        self._update_ui()

    # Udpate the UI
    def _update_ui(self):
        try:
            # Update frames
            self._messages_frame.update_msg()
            open_orders = self._strategy.get_value('open_orders')
            self._open_orders_frame.update(open_orders)
            self._strategy_frame.update_orders()
            self._strategy_frame.update_pnl()

        except RuntimeError as e:
            logger.error("Error while updating interface: %s", e)
            # Loop on itself after x milliseconds
        self.after(1500, self._update_ui)

