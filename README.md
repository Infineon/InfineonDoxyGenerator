# well-automated-documentation

This repository provides scripts (under [docs](https://github.com/Infineon/well-automated-documentation/tree/master/docs)) to generate documentation for XMC's Arduino libraries automatically. This repo is cloned into by travis when a library is updated. An example of the travis setup can be found at [.travis.yml](https://github.com/Infineon/TLE493D-W2B6-3DMagnetic-Sensor/blob/master/.travis.yml)

Simply copy the [.travis.yml](https://github.com/Infineon/TLE493D-W2B6-3DMagnetic-Sensor/blob/master/.travis.yml) file to another repository and modify the following variables:
* Github access token (the string after `env:global:secure`)
  * install travis client
  * Get your access token [here](https://github.com/settings/tokens) and run `travis encrypt GH_REPO_TOKEN=<copied_personal_acces_github_token>` under the **library repository**. The encryption must be done in the library repository (for example, TLE-xxx) since travis needs this token to push (from the library repo) to this repo. Each libary hasits own encryption/decryption key, thus only the library repo will have access to the decrypted token.
  * replace the string with the newly generated one
* PLATFORMIO_CI_SRC: the examples to be built

# TODO
Update images in the img folder and make sure they have meaningful names that corresponds to each sensor library.
