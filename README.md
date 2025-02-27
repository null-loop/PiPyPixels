## TODO List

Reimplement from [12-pinch](https://github.com/null-loop/12-pinch) - but better!

* [ ] 4 x 4 matrix wrapper - [RGB LED Driver](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/c%23)
* [ ] Startup / test screen
* [ ] Game engine / screen infra to run Game of Life
* [ ] Screen controller + GameScreen
* [ ] Remote control basics
* [ ] Frame rate control
* [ ] Power
* [ ] Zoom
* [ ] Brightness
* [ ] Local UI that mimics the LED Matrix + remote buttons ([DearPyGui](https://github.com/hoffstadt/DearPyGui))
* [ ] Maze Solver
* [ ] Screen navigation
* [ ] Snakes
* [ ] Pause / Play
* [ ] Step Forward
* [ ] ImageScreen
* [ ] Secret management approach
* [ ] Spotify - Need a Spotify client
* [ ] GitStatus - Need a Git client
* [ ] Options menu system
* [ ] Options menu for snake config
* [ ] Options menu for GOL presets

## Package List (To be confirmed as we go)

* CairoSVG
* PIL
* PyGithub
* mahotas
* numpy
* keyboard

## Future - making it useful for others...

* [ ] Documentation on my setup
* [ ] Where to get config from?
* [ ] Configurable matrix wrapper - max 1 channel
* [ ] Extract bits of matrix config to external source - _exhaustive_ coverage of underlying library configuration
* [ ] Extract screen setup to external config
* [ ] Configurable remote scan code to command mapping
* [ ] Local setup script?
* [ ] Script / CLI tool for capturing scan codes to config
* [ ] Re-setup from scratch on a new diet-pi image - document the whole process, reset when it goes wrong and get the docs right!
