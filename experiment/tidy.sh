
# ---------------------------------------------------------------------------- #

# move some stuffs around on server 

# ! change path
cd /data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images

this_model_name='k0-thresh0.0-diff'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name

this_model_name='k0-thresh0.0-cutbfscale10.0-diff'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name

this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name

# 50 70 90 110 130 150

for cut in '50.0' '70.0' '90.0' '110.0' '130.0' '150.0'
do 
this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-round0.3'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name
this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-diff'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name
done 

# ---------------------------------------------------------------------------- #

# ! copy to pc 

where=/cygdrive/c/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images
mkdir $where
for this_model_name in 'k0-thresh0.0-diff' 'k0-thresh0.0-cutbfscale10.0-diff' 'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff'
do
cd $where
mkdir $where/$this_model_name
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/$this_model_name/*png $where/$this_model_name
done 

for cut in '50.0' '70.0' '90.0' '110.0' '130.0' '150.0'
do 
this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-diff'
cd $where
mkdir $where/$this_model_name
scp -r $helix:$datadir/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/$this_model_name/*png $where/$this_model_name
done 
