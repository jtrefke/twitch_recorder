#!/bin/bash

INSTALL_APP_DIR=/opt/twitch_recorder
INSTALL_BIN_DIR=/usr/bin
TWITCH_USER_DATA_DIR="${HOME}/twitch_recorder"

if [ $(id -u) -ne 0 ]; then
  echo "Installing twitch recorder for user ${USER} only..."
  INSTALL_APP_DIR="${HOME}/twitch_recorder/app"
  INSTALL_BIN_DIR="${HOME}/bin"
else
  echo "Installing twitch recorder on computer globally..."
fi

echo "Installing twitch recorder to '${INSTALL_APP_DIR}'"

[ ! -d "${INSTALL_APP_DIR}" ] && mkdir -p "${INSTALL_APP_DIR}"
[ ! -d "${INSTALL_BIN_DIR}" ] && mkdir -p "${INSTALL_BIN_DIR}"

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cp -R ${SCRIPT_DIR}/* "${INSTALL_APP_DIR}"
chmod +x ${INSTALL_APP_DIR}/bin/*

ln -s ${INSTALL_APP_DIR}/bin/* "${INSTALL_BIN_DIR}"


mkdir -p "${TWITCH_USER_DATA_DIR}"
touch "${TWITCH_USER_DATA_DIR}/twitch_usernames.txt" # && chmod 777 "${TWITCH_USER_DATA_DIR}/twitch_usernames.txt"
