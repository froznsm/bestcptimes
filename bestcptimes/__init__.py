import asyncio

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from .view import BestCpTimesWidget
from .view import CpTimesListView


class BestCpTimes(AppConfig):
    game_dependencies = ['trackmania']
    app_dependencies = ['core.maniaplanet', 'core.trackmania']

    best_cp_times = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number_of_checkpoints = None
        self.best_cp_times = []  # List of PlayerCP Objects
        self.widget = None

    async def on_start(self):
        self.instance.signal_manager.listen(tm_signals.waypoint, self.player_cp)
        self.instance.signal_manager.listen(mp_signals.player.player_connect, self.player_connect)
        self.instance.signal_manager.listen(mp_signals.map.map_begin, self.map_begin)

        self.best_cp_times.clear()
        self.widget = BestCpTimesWidget(self)
        asyncio.ensure_future(self.widget.display())

    # When a player passes a CP
    async def player_cp(self, player, raw, *args, **kwargs):
        cpnm = int(raw['checkpointinlap'])
        laptime = int(raw['laptime'])
        pcp = PlayerCP(player, cpnm, laptime)
        if not self.best_cp_times or len(self.best_cp_times) <= cpnm:
            self.best_cp_times.append(pcp)
        elif self.best_cp_times[cpnm].time > laptime:
            self.best_cp_times[cpnm] = pcp
        await self.widget.display()

    # When the map ends
    async def map_begin(self, *args, **kwargs):
        self.best_cp_times.clear()
        await self.widget.display()

    # When a player connects
    async def player_connect(self, player, **kwargs):
        await self.widget.display(player)


# PlayerCP Event mapping a player to a cp and a time
class PlayerCP:
    def __init__(self, player, cp=0, time=0):
        self.player = player
        self.cp = cp
        self.time = time

