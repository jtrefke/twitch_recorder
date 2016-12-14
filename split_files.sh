#!/bin/bash
convertsecs() {
    h=`expr $1 / 3600`
    m=`expr $1  % 3600 / 60`
    s=`expr $1 % 60`
    printf "%02d:%02d:%02d\n" $h $m $s
}

split_video() {
  master=$1
  output=$2
  start=$3
  len=$4

  if [ -s $output ]; then
    return 0
  else
    exec ffmpeg -i $master -vcodec copy -ss $start -t $len $output &
    wait $!;
    return 1
  fi
}

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
FILES=$(ls raw/*.mp4|sort)

for FILE in $FILES
do
  FILE=$(basename $FILE)
  FOLDER="splits/${FILE}-chop"
  mkdir -p ${FOLDER}

  LENGTH=$(ffprobe -i "./raw/${FILE}" -show_entries format=duration -v quiet -of csv="p=0")
  LENGTH=${LENGTH%%.*} # remove decimal from microtime
  COUNTER=$LENGTH
  STARTTIME=0
  CUTTIME=3600
  TOTAL=1
  SPLITS=0

  # SPLIT IN HOUR CHUNKS
  while [ $COUNTER -gt 3600 ]; do
    split_video "./raw/${FILE}" "./${FOLDER}/${TOTAL}- ${FILE}" $(convertsecs $STARTTIME) 01:00:00
    [[ $? -eq 1 ]] && let SPLITS=$SPLITS+1
    let STARTTIME=$STARTTIME+3600
    let CUTTIME=$CUTTIME+3600
    let COUNTER=$COUNTER-3600
    let TOTAL=$TOTAL+1
  done
  # PROCESS LAST CHUNK - which is likely under an hour. Uses COUNTER which is the file's remaining  time
  split_video "./raw/${FILE}" "./${FOLDER}/${TOTAL}- ${FILE}" $(convertsecs $STARTTIME) $(convertsecs $COUNTER)
  [[ $? -eq 1 ]] && let SPLITS=$SPLITS+1

done

printf "\n"
printf "Operation Complete\n"
printf "Converted ${SPLITS} file(s)\n"

IFS=$SAVEIFS
