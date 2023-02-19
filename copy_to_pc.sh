

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images
criteria=k0-thresh0.0-avepix0.2-smoothave-pixcutave170.0-round0.3

# k0-thresh0.0-avepix0.2-smoothave-pixcutave170.0-round0.3
# 110

mkdir $criteria
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images/$criteria'_seg_ave'*.png $criteria # _seg_ave _img_ave


# ---------------------------------------------------------------------------- #

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
criteria=k0-thresh0.0-avepix0.2-smoothave-pixcutave170.0-round0.3

# k0-thresh0.0-avepix0.2-smoothave-pixcutave45.0-round0.3
# 110

mkdir $criteria
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/$criteria'_seg_ave'*.png $criteria # _seg_ave _img_ave


# _img_ave

# ---------------------------------------------------------------------------- #

mkdir /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/CompareGroupSameImgSlide2
cd /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/CompareGroupSameImgSlide2
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/CompareGroupSameImgSlide2/*png . 

