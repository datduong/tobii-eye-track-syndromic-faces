

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
criteria=nosmooth-thresh0.0-avepix0.3-round0.7
mkdir $criteria
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/$criteria'_seg_ave'*.png $criteria


# ---------------------------------------------------------------------------- #

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2/*png . 

