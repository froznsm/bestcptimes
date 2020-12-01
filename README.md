This app will be part of the 0.5.0 release of [PyPlanet](http://pypla.net). This repo will probably not be maintained.

# BestCPTimes
App for [PyPlanet](http://pypla.net).
## Description
BestCPTimes is an app for [PyPlanet](http://pypla.net) for use in Trackmania TimeAttack. It displays the best driven times at every checkpoint at the top of the UI.
### List UI
When clicking on the 'Best CPs' header a list of all the checkpoints and times as well as nicknames is shown. This is useful because the display at the top is capped at 30 checkpoints to retain visibility. If the map has more checkpoints using something like [currentcps](https://github.com/teemann/currentcps) is recommended.
### Laps
The `laptime` component of the `waypoint` callback is used to avoid adding new checkpoints each lap.
