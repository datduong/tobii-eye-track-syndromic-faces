
cd C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/aoi_segmentation

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir 25radius-fix-mismatch-name-to-csv-04042023 --where_to_save_formated_individual 25radius-fix-mismatch-name-csv-noave-whtbg-04042023 --imsize 720,720 

python get_remove_average_tobii.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Peter25RadiusTobiiHeatmap04042023 --where_to_save_formated_individual 25radius-peter-noave-whtbg-04042023 --imsize 720,720 


cd C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-noave-whtbg-04042023 --final_output_dir 25rad-nih-noave-byaccuracy-04042023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimple.csv

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-peter-noave-whtbg-04042023 --final_output_dir 25rad-peter-noave-byaccuracy-04042023 --add_file_name_pattern .png
# --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimplePeter.csv

