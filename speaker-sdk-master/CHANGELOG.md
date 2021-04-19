## 2021-02-26
### Added

- Added possibility to select (partner) specific services.

- Added script `examples/list_services.py` to list available services.

- Added script `examples/keycloak_login.py` to retrieve JSON web token for the specified user.

- Added option to all example clients to access the Speaker Cluster via username+password, instead of an JSON web token.

## 2021-02-12
### Changed

- Replaced `resampy` with `samplerate` as it was causing some trouble depending on the combination of Python versions and Operating Systems.

### Fixed

- Fixed bug in `speech_recognition.py` where the client would close the connection before receiving the transcripts, if an audio file is sent to the backend. 

- Fixed bug in `speech_recognition.py` where it crashed when using audio files with multiple channels. Now, the first channel is used by default.

- Adapted `server_mockup.py` to properly reflect the behavior of the backend when accessing it with `speech_recognition.py`.