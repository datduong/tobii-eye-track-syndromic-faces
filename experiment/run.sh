
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/format_heatmap

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir 25radius-fix-mismatch-name-to-csv-04042023 --where_to_save_formated_individual 25radius-fix-mismatch-name-csv-noave-whtbg-04042023 --imsize 720,720 

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Peter25RadiusTobiiHeatmap04042023 --where_to_save_formated_individual 25radius-peter-noave-whtbg-04042023 --imsize 720,720 


cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-fix-mismatch-name-csv-noave-whtbg-04042023 --final_output_dir 25rad-nih-noave-byaccuracy-04042023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimple.csv

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source 25radius-peter-noave-whtbg-04042023 --final_output_dir 25rad-peter-noave-byaccuracy-04042023 --add_file_name_pattern .png
# --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimplePeter.csv

# ---------------------------------------------------------------------------- #

cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/format_heatmap

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Heatmap25rExpert04172023 --where_to_save_formated_individual Heatmap25rExpertNoAve04172023 --imsize 720,720 

python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Heatmap25rNonExpert04172023 --where_to_save_formated_individual Heatmap25rNonExpertNoAve04172023 --imsize 720,720 



cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data

python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source Heatmap25rExpertNoAve04172023 --final_output_dir Heatmap25rExpertNoAveByAcc04172023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimpleNihPeter04172023.csv --add_file_name_pattern _25r


python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source Heatmap25rNonExpertNoAve04172023 --final_output_dir Heatmap25rNonExpertNoAveByAcc04172023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimpleNihPeter04172023.csv --add_file_name_pattern _25r



# ! keep average experts
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/format_heatmap
python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Heatmap25rExpert04172023 --where_to_save_formated_individual Heatmap25rExpertKeepAve04172023 --imsize 720,720 --keep_average

cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data
python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source Heatmap25rExpertKeepAve04172023 --final_output_dir Heatmap25rExpertKeepAveByAcc04172023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimpleNihPeter04172023.csv --add_file_name_pattern _25r


# ! keep average nonexperts
cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/format_heatmap
python get_remove_average_heatmap.py --main_datadir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --imdir Heatmap25rNonExpert04172023 --where_to_save_formated_individual Heatmap25rNonExpertKeepAve04172023 --imsize 720,720 --keep_average

cd C:/Users/duongdb/Documents/GitHub/tobii-eye-track-syndromic-faces/check_data
python move_images.py --main_dir C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023 --source Heatmap25rNonExpertKeepAve04172023 --final_output_dir Heatmap25rNonExpertKeepAveByAcc04172023 --df C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimpleNihPeter04172023.csv --add_file_name_pattern _25r

