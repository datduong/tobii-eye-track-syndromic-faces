

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
criteria=k0-thresh0.0-avepix0.2-smoothave-pixcutave0.7-diff
mkdir $criteria
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/$criteria'_img_ave'*.png $criteria


# ---------------------------------------------------------------------------- #

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2/*png . 

