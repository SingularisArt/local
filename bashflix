#!/usr/bin/env bash

#set -exu

SELECT=false
PLAYER="vlc"
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -h|--help)
      echo -n "
      ██████╗  █████╗ ███████╗██╗  ██╗███████╗██╗     ██╗██╗  ██╗
      ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║╚██╗██╔╝
      ██████╔╝███████║███████╗███████║█████╗  ██║     ██║ ╚███╔╝ 
      ██╔══██╗██╔══██║╚════██║██╔══██║██╔══╝  ██║     ██║ ██╔██╗ 
      ██████╔╝██║  ██║███████║██║  ██║██║     ███████╗██║██╔╝ ██╗
      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝

      "
      echo "Video streaming on MacOS and Linux, with subtitles."
      echo 
      echo "Quick start: bashflix \"QUERY\" [SUBTITLES_LANGUAGE]"
      echo "       e.g.: bashflix \"serie s01e01 1080p\" en"  
      echo 
      echo "Usage: 'bashflix [COMMAND] [OPTIONS]'"
      echo
      echo "Commands:"
      echo "  update                                  Update bashflix"
      echo "  previously                              Previously watched"
      echo "  select \"QUERY\" [SUBTITLES_LANGUAGE]   Select torrent from list"
      echo 
      echo "Options:"
      echo "  -h, --help            See this text"
      echo "  -p, --player PLAYER   Specify the player"
      echo
      echo "Not working?"
      echo "  * Run 'bashflix update';"
      echo "  * Add 'select' before \"QUERY\";"
      echo "  * Pause video and wait a bit;"
      echo "  * To sync subtitles, press 'j' to speed it up or 'h' to delay it."
      echo "  * Change DNS to 1.1.1.1 - https://1.1.1.1/dns/"
      echo "  * Please report the issue here: https://github.com/0zz4r/bashflix/issues/new/choose"
      echo
      exit 0
      ;;
    u|update)
      bash -c "$(curl -s https://raw.githubusercontent.com/0zz4r/bashflix/master/install.sh)"
      echo "Updated!"
      exit 0
      ;;
    p|previously)
      echo "Previously watched:"
      echo "$(head ~/bashflix_previously.txt)"
      exit 0
      ;;
    s|select)
      SELECT=true
      QUERY="$2"
      if [ -n "$2" ] && [[ "$2" != *"-"* ]]; then
        SUBTITLES_LANGUAGE="$3"
        shift
      fi
      shift # past argument
      shift # past value      
      ;;
    -p|--player)
      PLAYER="$2"
      shift
      shift
      ;;
    *)    # unknown option
      #POSITIONAL+=("$1") # save it in an array for later
      #shift # past argument

      QUERY="$1"
      if [ -n "$2" ] && [[ "$2" != *"-"* ]]; then
        SUBTITLES_LANGUAGE="$2"
        shift
      fi
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

query="${QUERY#\ }"
query="${query%\ }"
query="${query// /.}"

if [ "$SELECT" = true ]; then
  out=$(pirate-get --total-results 10 -C 'echo "%s"' "${query}" | tail -n 1)
  magnet="${out:2}"
else
  magnet=$(pirate-get --total-results 10 -0 -C 'echo "%s"' "${query}" | tail -n 1)
  if [ -z $magnet ]; then
    echo "Not Found."
    exit 1
  else
    echo "${magnet}"
  fi
fi

echo "${query}" | cat - ~/bashflix_previously.txt > temp && mv temp ~/bashflix_previously.txt

if [ -n "${SUBTITLES_LANGUAGE}" ]; then
  torrent_name_param=$(awk -F "&" '{print $2}' <<< "$magnet")
  torrent_name_dirty=$(awk -F "=" '{print $2}' <<< "$torrent_name_param")
  torrent_name_raw=$(echo "${torrent_name_dirty}" | sed -e 's/%\([0-9A-F][0-9A-F]\)/\\\\\x\1/g')
  torrent_name_escaped=$(echo -e "${torrent_name_raw}")
  torrent_name=$(echo -e "${torrent_name_escaped}")
  mkdir -p "/tmp/bashflix/${query}"
  languages=("${SUBTITLES_LANGUAGE}" "en")
  echo "Searching subtitles for ${torrent_name}"
  for language in ${languages[@]}; do
    subliminal --opensubtitles 0zz4r R4zz0___ download -l "${language}" -p opensubtitles -d "/tmp/bashflix/${query}" "${torrent_name}"
    find /tmp/bashflix/${query} -maxdepth 1 -name "*${language}*.srt" | head -1 | xargs -I '{}' mv {} "/tmp/bashflix/${query}/${query}.${language}.srt"
    subtitle=$(find /tmp/bashflix/${query} -maxdepth 1 -name "${query}.${language}.srt" | head -1)
    if [ -n "${subtitle}" ]; then
      echo "Found ${language} subtitles"
      break;
    fi
  done
fi

if [ -z "${subtitle}" ]; then
  peerflix "${magnet}" -n -r --"${PLAYER}" -- --fullscreen
else
  peerflix "${magnet}" -n -r -t "${subtitle}" --"${PLAYER}" -- --fullscreen 
fi
