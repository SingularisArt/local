#!/usr/bin/env bash

source ~/.config/zsh/exports.zsh

clock=$(date '+%I')

current_date=$(date "+%b %d %Y")
time=$(date "+%I:%M %p")

echo "${current_date} (${time})"
