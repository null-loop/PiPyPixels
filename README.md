## TODO List

Reimplement from [12-pinch](https://github.com/null-loop/12-pinch) - but better!

* [x] 2 x 2 matrix wrapper - [RGB LED Driver](https://github.com/hzeller/rpi-rgb-led-matrix) - configurable size! Must be regular
* [x] Startup / test screen
* [x] Local UI that mimics the LED Matrix + remote buttons ([DearPyGui](https://github.com/hoffstadt/DearPyGui))
* [x] Game engine / screen infra to run Game of Life
* [x] Screen controller + GameScreen
* [x] StartupScreen + ImageScreen
* [x] Remote control basics
* [x] Screen navigation
* [x] Frame rate control
* [x] Zoom
* [x] Reset
* [x] Pause / Play
* [x] Step Forward
* [x] Power
* [x] Brightness
* [x] Maze Solver
* [x] Snakes
* [x] pause_and_wait() methods
* [x] Ensure we're using commands everywhere we can - review use of the above method!
* [x] Write game startups to fresh canvas (Snake / Maze / Life) - won't affect local
* [x] Scale image StartupScreen
* [x] pi-test.py
* [x] StartupScreen needs to remove itself from the screens when navigated away from / after a time period
* [x] ArtworkScreen
* [x] Show StartupScreen on Power On
* [x] Screen capture in local
* [ ] Options types
* [ ] Reading config from JSON
* [ ] Secret management approach
* [ ] Spotify - Need a Spotify client
* [ ] GitStatus - Need a Git client
* [ ] Options 'screens' or Webserver?
* [ ] setup.py

## Package List (To be confirmed as we go)

* [x] Pillow
* [x] DearPyGui
* [ ] PyGithub
* [ ] mahotas
* [x] numpy
* [x] keyboard
* [ ] Spotipy

## Future - making it useful for others...

* [ ] Documentation on my setup
* [ ] Where to get config from?
* [ ] Configurable matrix wrapper - max 1 channel - this is started
* [ ] Extract bits of matrix config to external source - _exhaustive_ coverage of underlying library configuration
* [ ] Extract screen setup to external config
* [ ] Configurable remote scan code to command mapping
* [ ] Local setup script?
* [ ] Script / CLI tool for capturing scan codes to config
* [ ] Re-setup from scratch on a new diet-pi image - document the whole process, reset when it goes wrong and get the docs right!

## Far Future - Cube Layout

* Can we drive a fifth panel?
* Design frame
  * expose PI ports, sit at bottom, 
  * cable management
  * magnetic mounting (inner metal plate), allows panel removal (requires sufficient length in cabling)
  * POWER! Need a single power source
* Different GameBoard
* Images render on each panel, carousel?
  * Radical change to the screen concept...

## Attribution

* [RGB LED Driver](https://github.com/hzeller/rpi-rgb-led-matrix) - Obvs.

## Known Issues

None - yet!