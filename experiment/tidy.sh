
# move some stuffs around 

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


for cut in '90.0' '70.0' '110.0'
do 
this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-round0.3'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name
this_model_name='k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave'$cut'-diff'
mkdir $this_model_name
mv Slide*$this_model_name*csv $this_model_name*png $this_model_name
done 
