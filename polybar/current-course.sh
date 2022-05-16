#!/usr/bin/env bash

source ~/.config/zsh/exports.zsh
name=$(cat ${CURRENT_COURSE}/info.yaml | shyaml get-value short)

echo "%{F#3A3B3C}${name}%{F-}"
