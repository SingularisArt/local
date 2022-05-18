#!/usr/bin/env bash

source ~/.config/zsh/exports.zsh
name=$(cat ${CURRENT_COURSE}/info.yaml | shyaml get-value title)

echo "${name}"
