
## Instruction 

We first outline the data processing step, and then the steps to compare visual heatmaps. **Note, please change your directory path accordingly.**

### Remove average heatmap (which focuses on mostly eyes/nose/mouth) from each image.

**We can do this on local computer so we can easily view the images.**

```bash
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/format_heatmap

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir 25radius-fix-mismatch-name-to-csv --where_to_save_formated_individual 25radius-fix-mismatch-name-csv-no-ave-whtbg --imsize 720,720 

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Peter25radiusTobiiHeatmap --where_to_save_formated_individual 25radius-no-ave-whtbg-nonclinicians --imsize 720,720 
```


### For each test image, put the corresponding Tobii eye-tracking output into 4 groups.

For a specific test image, there will be 4 groups each for the clinicians (and likewise for the nonclinicians ):
- Group 1: clinicians who correctly identify the image is affected vs unaffected
- Group 2: clinicians who incorrect identify the image is affected vs unaffected
- Group 3: clinicians who correctly identify the image is affected vs unaffected, AND said the correct disease name
- Group 4: clinicians who correctly identify the image is affected vs unaffected, BUT said the incorrect disease name

**We can do this on local computer so we can easily view the images.**

```bash
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-no-ave-whtbg --final_output_dir eye_track_data_without_ave_signal --df C:/Users/duongdb/Documents/TOBII_DATA_PATH/eye_track_record_accuracy_per_person.csv.csv

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-no-ave-whtbg-nonclinicians --final_output_dir eye_track_data_without_ave_signal_nonclinicians --df C:/Users/duongdb/Documents/TOBII_DATA_PATH/eye_track_record_accuracy_per_person.csv --add_file_name_pattern .png
```


### Compare 2 sets of participants.

We should do this on server, we don't need cuda, simple cpu will work fast enough (2-3 hours at most). All paths will now be with respect to server path instead of local pc computer c:/user/something.

We run python code to create a bunch of bash script, this code will auto submit the bash script. We need to provide command to submit job according to the server specification (see line with `os.system` in this code).

The line `slide_folders` will select with slide (in other word, which image) we want to compare clinician vs nonclinician group. The line `for group in ['Group1']` will indicate which group (there are 4 possible groups).  


```bash
cd tobii-eye-track-syndromic-faces/experiment
python group_vs_group_same_img_heatmap.py # need to change paths inside this code
```
 
After this step, we will see the heatmap averaged over clinician participants (and likewise for nonclinician group). The average heatmap will be with respect to the specific setting to smooth images and scale color intesity and so forth. 

Output will be saved at the variable `$output_dir` in `group_vs_group_same_img_heatmap.py`; for example, output dir can be `/data/duongdb/TOBII_DATA_PATH/eye_track_data_without_ave_signal/Compare_clinicians_vs_not/Slide1`

See example output below. The png outputs are the heatmaps averaged over clinician group1 (and likewise nonclinician group1). The csv outputs compare the differences between the average of the clinician group1 vs nonclinician group1. We use many different settings to smooth and scale the Tobii heatmaps, and these settings are shown the output names. See more comments about these settings in `tobii-eye-track-syndromic-faces/experiment/group_vs_group_same_img_heatmap.py`. 

<!-- ![example1](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/ExampleOutputDir.PNG) -->


### Combine all the csv outputs into a single place to analyze.

It's much easier to create the forest plot (from meta-analysis) if we combine all the individual csv into a single larger csv. 

```bash
cd tobii-eye-track-syndromic-faces/tally_csv
python clinician_vs_not_on_same_img.py # need to change paths inside this code
```

<!-- We should see this `Group1VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv` (and other csv files). ***Because of bootstrap, we may not see the exact same numbers in the .csv every time; however, the output should be consistent enough between each repetition.***

![example2](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/ExampleAfterCombineCsv.PNG) -->

### Make meta-analysis plot in R.

We do this on local computer so we can easily view the plots. Use `meta_analysis/clinician_vs_not_on_same_img.R`. 

Variables to change in this .R code are: [`data_path` and `what_group`]. `threshold_used` defines the intensity where we truncate eye heatmap, and `mod` is the corresponding outputs. 

<!-- Unless we have our own modified experiments, `threshold_used` and `mod` don't need to be changed, since these outputs were already defined in `group_vs_group_same_img_heatmap.py`. We should see this output. 

![example3](https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/img/Group1-clinicians-nonclinicians-IoU-thr0.png) -->



