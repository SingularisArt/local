#!/usr/bin/bash

change_icon() {
  if (($(ps -aux | grep [p]icom | wc -l) > 0)); then
    icon=""
  else
    icon=""
  fi
}

if [[ $(ps -aux | grep picom | wc -l) > 1 ]]; then
  pkill -9 picom
  notify-send -u low 'picom' "Blur Disabled"
else
  picom -b --config ~/.config/picom/picom.conf --experimental-backends --backend glx --blur-method dual_kawase &
  notify-send -u low 'picom' "Blur Enabled"
fi

change_icon
echo ${icon}
