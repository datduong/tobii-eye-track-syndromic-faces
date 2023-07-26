

### Remove average heatmap (which focuses on mostly eyes/nose/mouth) from each image.

**We can do this on local computer so we can easily view the images.**

```bash
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/aoi_segmentation

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir 25radius-fix-mismatch-name-to-csv --where_to_save_formated_individual 25radius-fix-mismatch-name-csv-no-ave-whtbg --imsize 720,720 

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Peter25radiusTobiiHeatmap --where_to_save_formated_individual 25radius-no-ave-whtbg-peter --imsize 720,720 
```


### Put images into 4 groups based on their accuracy.

**We can do this on local computer so we can easily view the images.**

```bash
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-no-ave-whtbg --final_output_dir RemoveAveEyeTrack --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimple.csv

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-no-ave-whtbg-peter --final_output_dir RemoveAveEyeTrackPeter --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimplePeter.csv --add_file_name_pattern .png
```


### Compare 2 sets of participants.

We should do this on server, we don't need cuda, simple cpu will work fast enough (2-3 hours at most). All paths will now be with respect to server path instead of local pc computer c:/user/something.

We run python code to create a bunch of bash script, this code will auto submit the bash script. We need to provide command to submit job according to the server specification (see line with `os.system` in this code).

The line `slide_folders` will select with slide (in other word, which image) we want to compare NIH vs Peter's group. The line `for group in ['Group1']` will indicate which group (there are 4 possible groups).  


```bash
cd tobii-eye-track-syndromic-faces/experiment
python group_vs_group_same_img_vsPeter.py # need to change paths inside this code
```
 
After this step, we will see the heatmap averaged over nih participants (and likewise for peter's group). The average heatmap will be with respect to the specific setting to smooth images and scale color intesity and so forth. 

Output will be saved at the variable `$output_dir` in `group_vs_group_same_img_vsPeter.py`; for example, output dir can be `/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgVsPeter/Slide1`

See example output below. The png outputs are the heatmaps averaged over NIH group1 (and likewise Peter group1). The csv outputs compare the differences between the average of the NIH group1 vs Peter group1. We use many different settings to smooth and scale the Tobii heatmaps, and these settings are shown the output names. See more comments about these settings in `tobii-eye-track-syndromic-faces/experiment/group_vs_group_same_img_vsPeter.py`. 

![example1](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/ExampleOutputDir.PNG)


### Combine all the csv outputs into a single place to analyze.

It's much easier to create the forest plot (from meta-analysis) if we combine all the individual csv into a single larger csv. 

```bash
cd tobii-eye-track-syndromic-faces/tally_csv
python tally_group_vs_group_same_img_vsPeter.py # need to change paths inside this code
```

We should see this `Group1VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv` (and other csv files). ***Because of bootstrap, we may not see the exact same numbers in the .csv every time; however, the output should be consistent enough between each repetition.***

![example2](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/ExampleAfterCombineCsv.PNG)

### Make meta-analysis plot in R.

We do this on local computer so we can easily view the plots. Use `meta_analysis/group_vs_group_same_imgVsPeter.R`. 

Variables to change in this .R code are: [`data_path` and `what_group`](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/meta_analysis/group_vs_group_same_imgVsPeter.R#L5). `threshold_used` defines the intensity where we truncate eye heatmap, and `mod` is the corresponding outputs. 

Unless we have our own modified experiments, `threshold_used` and `mod` don't need to be changed, since these outputs were already defined in `group_vs_group_same_img_vsPeter.py`. We should see this output. 

![example3](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/Group1-NIH-Peter-IoU-thr0.png)

### Plot Tobii heatmap on top the original image. 

We will add more instruction soon. 


