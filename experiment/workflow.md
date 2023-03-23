
# ---------------------------------------------------------------------------- #
# Remove average heatmap from each image

CAN DO THIS ON LOCAL COMPUTER SO WE CAN EASILY VIEW THE IMAGES

cd C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/aoi_segmentation

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir 25radius-fix-mismatch-name-to-csv --where_to_save_formated_individual 25radius-fix-mismatch-name-csv-no-ave-whtbg --imsize 720,720 

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Peter25radiusTobiiHeatmap --where_to_save_formated_individual 25radius-no-ave-whtbg-peter --imsize 720,720 


# ---------------------------------------------------------------------------- #
# ! put images into 4 groups based on their accuracy

# ! CAN DO THIS ON LOCAL COMPUTER SO WE CAN EASILY VIEW THE IMAGES

cd C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-no-ave-whtbg --final_output_dir RemoveAveEyeTrack --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimple.csv

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-no-ave-whtbg --final_output_dir RemoveAveEyeTrackPeter --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimplePeter.csv --add_file_name_pattern .png


# ---------------------------------------------------------------------------- #
# ! compare 2 sets of participants 

# ! SHOULD DO THIS ON SERVER. DON'T NEED CUDA, SIMPLE CPU WILL WORK FAST ENOUGH (2-3 HOURS AT MOST)

# ! ALL PATH WILL NOW BE WITH RESPECT TO SERVER PATH INSTEAD OF LOCAL PC COMPUTER C:/USER/SOMETHING
# run python code to create a bunch of bash script, this python will auto submit the bash script. we need to provide command to submit job according to the server specification 

cd Tobii-AOI-FaceSyndromes/experiment
group_vs_group_same_img_vsPeter.py # should just copy/paste code into the terminal, don't need to make this a script. 

# ---------------------------------------------------------------------------- # 
# ! after this step, we will see the heatmap averaged over nih participants (and likewise for peter's group)
# ! the averaged heatmap will be with respect to the specific setting to smooth images and scale color intesity and so forth. 

output will be saved at the variable $output_dir in group_vs_group_same_img_vsPeter.py; for example, /data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgVsPeter/Slide1


# ---------------------------------------------------------------------------- #
# ! combine all the csv outputs into a single place to analyze 
# ! it's much easier to create the forest plot (from meta-analysis) if we combine all the individual csv into a single larger csv. 

cd Tobii-AOI-FaceSyndromes/tally_csv
tally_group_vs_group_same_img_vsPeter.py # should just copy/paste into the terminal, don't need to make this a script. 

# ! to make the meta-analysis plot in R, we do this on local computer.
use meta_analysis/group_vs_group_same_imgVsPeter.R

# ---------------------------------------------------------------------------- #

# ! COPY OUTPUT INTO LOCAL COMPUTER, EASIER TO VIEW IMAGES AND MAKE POWERPOINT 


