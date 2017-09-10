import asyncio
import logging

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
        self.instance.signal_manager.listen(mp_signals.map.map_start__end, self.map_end)
        self.best_cp_times.clear()
        self.widget = BestCpTimesWidget(self)
        asyncio.ensure_future(self.widget.display())

    # When a player passes a CP
    async def player_cp(self, player, race_time, raw, *args, **kwargs):
        cpnm = int(raw['checkpointinlap'])
        laptime = int(raw['laptime'])
        pcp = PlayerCP(player, cpnm+1, laptime)
        if not self.best_cp_times or len(self.best_cp_times) <= cpnm:
            self.best_cp_times.append(pcp)
            logging.debug('new cp was added!!!!!')
            logging.debug(' '.join(str(e.time) for e in self.best_cp_times))
        elif self.best_cp_times[cpnm].time > laptime:
            self.best_cp_times[cpnm] = pcp
            logging.debug('checkpoint '+str(cpnm+1)+' was changed')
            logging.debug(' '.join(str(e.time) for e in self.best_cp_times))
        await self.widget.display()

    # When the map ends
    async def map_end(self, *args, **kwargs):
        self.best_cp_times.clear()
        await self.widget.display()

    # When a player connects
    async def player_connect(self, player, **kwargs):
        await self.widget.display(player)

    # TODO: to be moved to .view in pyplanet 0.7.0 or earlier
    async def show_cptimes_list(self, player, data=None, **kwargs):
        view = CpTimesListView(self)
        await view.display(player=player.login)
        return view


class PlayerCP:
    def __init__(self, player, cp=0, time=0):
        self.player = player
        self.cp = cp
        self.time = time


class VirtualPlayer:
    def __init__(self, nickname, login):
        self.nickname = nickname
        self.login = login
