
# ---------------------------------------------------------------------------- #

# ! move some stuffs around on server 

# ! change path
maindir=/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertKeepAveByAcc04172023
subdir=CompareGroupSameImg

cd $maindir

this_model_name='k0-thresh0.0-diff'
mkdir $this_model_name
for slide in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 
do
  mv $subdir'Slide'$slide'/'*$this_model_name*png $this_model_name
done 

# this_model_name='k0-thresh0.0-cutbfscale10.0-diff'
# mkdir $this_model_name
# for slide in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 
# do
#   mv $subdir'Slide'$slide'/'*$this_model_name*png $this_model_name
# done 

this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff'
mkdir $this_model_name
for slide in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 
do
  mv $subdir'Slide'$slide'/'*$this_model_name*png $this_model_name
done 

for cut in '50.0' '70.0' '90.0' '110.0' '130.0' '150.0'
do 

  this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-round0.3'
  mkdir $this_model_name

  for slide in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 
  do
    mv $subdir'Slide'$slide'/'*$this_model_name*png $this_model_name
  done 

  this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-diff'
  mkdir $this_model_name

  for slide in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 
  do
    mv $subdir'Slide'$slide'/'*$this_model_name*png $this_model_name
  done

done 

# ---------------------------------------------------------------------------- #

# ! copy to pc 

# ! condition on experts (or nonexperts), compare how succ vs underperforming do. 
scp $helix:$datadir/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/all_img_nonexpgroup_succ_vs_under_long.csv /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023

# ! condition on one image, compare experts vs nonexperts 
scp $helix:$datadir/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023/*csv /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023

# ! compare vs saliency 
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Compare2Saliency /cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/
