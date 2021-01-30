python Crop.py $1
python ocr.py --image $2 --preprocess $3
echo "*****Welcome To Translation*****"

python /home/dell/rest-app/app.py &
gnome-terminal -x sh -c "python /home/dell/Desktop/project/new.py; bash"

