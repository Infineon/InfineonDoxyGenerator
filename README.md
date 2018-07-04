# well-automated-documentation

This repository provides scripts (under [docs](https://github.com/Infineon/well-automated-documentation/tree/master/docs)) to generate documentation for XMC's Arduino libraries automatically. This repo is cloned into by travis when a library is updated. An example of the travis setup can be found at [.travis.yml](https://github.com/Infineon/TLE493D-W2B6-3DMagnetic-Sensor/blob/master/.travis.yml)

Simply copy the [.travis.yml](https://github.com/Infineon/TLE493D-W2B6-3DMagnetic-Sensor/blob/master/.travis.yml) file to another repository and modify the following variables:
* Github access token (the string after `env:global:secure`)
  * install travis client
  * Get your access token [here](https://github.com/settings/tokens) and run `travis encrypt ***` under the library repository
  * replace the string with the newly generated
* REPO_NAME: the name of the generated library = the name of the repository
* PLATFORMIO_CI_SRC: the examples to be built

