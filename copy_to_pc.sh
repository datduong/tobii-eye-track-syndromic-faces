

cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Diseases
mkdir thresh0.1-avepix0.2-round0.35_seg_ave
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/*thresh0.1-avepix0.2-round0.35_seg_ave*.png thresh0.1-avepix0.2-round0.35_seg_ave


# ---------------------------------------------------------------------------- #

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgSlide2/*png . 

