#!/bin/bash

set -e

BATCH=5
MODELDIR=models-DF2K/
VIDEOFILE="$2"
INPUTFPS=$3
if [ -z "${INPUTFPS}" ]; then
    INPUTFPS=`ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate $VIDEOFILE | awk -F / '{print $1/$2}'`
fi
INTERP=nn

echo "Super-Resolution in $VIDEOFILE @ ${INPUTFPS} fps using ${MODELDIR}"

mkdir -p frames-tmp

rm -f done.log
touch done.log

LINES=`ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=nb_frames $VIDEOFILE | tr -d '\r'`
FRAMES=$(( $LINES / $BATCH ))

# 启动 RTSP 流服务器
#./live555MediaServer

for((i=0;i<$FRAMES;i++))
do
    seq -f "%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) | xargs -I{} sh -c 'ffmpeg -v error -stats -y -nostdin -ss $(echo {} / '$INPUTFPS' | bc -l) -i '"$VIDEOFILE"' -vf "select=gte(frame\<={}/${INPUTFPS}, n_forced=1), scale=360:-1" -q:v 1 -r '$INTERP' frames-tmp/frame-%06d.jpg && echo {} >> done.log'
done

GOT=`cat done.log | wc -l`
ALL=`echo "scale=2;$LINES/${INPUTFPS}" | bc | awk '{print int($1+0.5)}'`
if (( $GOT < $ALL )); then
    echo "Failed to extract $ALL frames from $VIDEOFILE at ${INPUTFPS}fps: got $GOT frames only"
    rm frames-tmp/*
    exit -1
else
    echo "Extracted $GOT frames from $VIDEOFILE at ${INPUTFPS}fps"
fi
rm done.log

rm -f "$1"
touch "$1"

for((i=0;i<$FRAMES;i++))
do
    OUTPUT=$1
    seq -f "%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) | xargs -I{} sh -c './rife-ncnn-vulkan -i frames-tmp/frame-{}.jpg -o frame-cv.png' > /dev/null
    seq -f "%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) | xargs -I{} sh -c './edvr-ncnn-vulkan -i frames-tmp/frame-{}.jpg -o frame-sr.png' > /dev/null
    seq -f "%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) | xargs -I{} sh -c './rife-ncnn-vulkan -i frames-tmp/frame-{}.jpg -o frame-cv.png -m 2' > /dev/null
    seq -f "frame-cv.png_%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) >> mix.input
    seq -f "frame-sr.png_%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) >> mix.input
    if (( $(($i*100%$FRAMES)) == 0 )); then
        echo -n $((($i*100)/$FRAMES))% ' '
    fi
done
echo
echo "Blending Frames"
./waifu2x-ncnn-vulkan -i mix.input -o mix-output.png -m noise_scale --scale 1 > /dev/null
rm -f mix.input

echo "Encoding Video Concatenation"
for((i=0;i<$FRAMES;i++))
do
    OUTPUT=$1
    seq -f "%06g" $(($i*$BATCH+1)) $(($i*$BATCH+$BATCH)) | xargs -I{} sh -c 'ffmpeg -v error -stats -y -nostdin -i frame-cv.png_{} -i mix-output.png_{} -i frame-sr.png_{} -filter_complex "[0][1]overlay=10:10:enable=\'between(t,2,5)\'[tmp],[2][1]overlay=10:346[over1];[over1][0]overlay=10:68:enable=\'between(t,5,8)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,8,11)\'[tmp],[2][1]overlay=10:346[over2];[over2][0]overlay=10:68:enable=\'between(t,11,14)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,14,16)\'[tmp],[2][1]overlay=10:346[over3];[over3][0]overlay=10:68:enable=\'between(t,16,17)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,17,20)\'[tmp],[2][1]overlay=10:346[over4];[over4][0]overlay=10:68:enable=\'between(t,20,22)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,22,25)\'[tmp],[2][1]overlay=10:346[over5];[over5][0]overlay=10:68:enable=\'between(t,25,28)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,28,31)\'[tmp],[2][1]overlay=10:346[over6];[over6][0]overlay=10:68:enable=\'between(t,31,34)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,34,37)\'[tmp],[2][1]overlay=10:346[over7];[over7][0]overlay=10:68:enable=\'between(t,37,40)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,40,43)\'[tmp],[2][1]overlay=10:346[over8];[over8][0]overlay=10:68:enable=\'between(t,43,46)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,46,49)\'[tmp],[2][1]overlay=10:346[over9];[over9][0]overlay=10:68:enable=\'between(t,49,52)\'[tmp];[0][1]overlay=10:10:enable=\'between(t,52,55)\'[tmp],[2][1]overlay=10:346[over10];[over10][0]overlay=10:68:enable=\'between(t,55,57)\'[tmp]" -vcodec libx264 -pix_fmt yuv420p -crf 18 -s 1280x720 -aspect 16:9 -vsync 1 -vtag hvc1 -t 0.04 -strict -2 -f h264 /dev/null && echo {} >> done.log'
done

GOT=`cat done.log | wc -l`
if (( $GOT < $LINES )); then
    echo "Failed to render $LINES frames to $OUTPUT"
    rm -f ${OUTPUT}
    exit -1
else
    echo "Rendered $GOT frames to $OUTPUT"
fi
rm done.log

rm -f frames-tmp/*
