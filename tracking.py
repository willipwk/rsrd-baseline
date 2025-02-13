import yaml
import json
import os
import glob


with open("partnet_mobility_data_split.yaml", "r") as f:
    data_config = yaml.safe_load(f)
test_video_list = data_config["test"]
dataset_config_path = "path/to/dataset/config/file"
with open(dataset_config_path, 'r') as f_dataset:
    dataset_config_dict = json.load(f_dataset)

for test_video_path in test_video_list:
    # may need to modify the test video path
    cat = test_video_path.split('/')[2]
    obj_id = test_video_path.split('/')[3]
    joint = test_video_path.split('/')[4]
    joint_id = int(joint[5:6])
    joint_type = None
    interaction_list = dataset_config_dict[cat][obj_id]["interaction"]
    for interaction in interaction_list:
        if joint_id == interaction["id"]:
            joint_type = interaction["type"]
    assert joint_type is not None, "cannot find joint in dataset config"

    test_scan_path = test_video_path[:test_video_path.rfind("view_")] + "view_init_rsrd/"
    outdir = f"outputs/{test_scan_path}"
    dig_path = f"{outdir}/dig/"
    dig_config_path_list = glob.glob(f"{dig_path}/*/config.yml")
    assert len(dig_config_path_list) > 0, "no dig config found"
    dig_config_path = dig_config_path_list[-1]

    is_obj_jointed = "True" if joint_type == "hinge" else "False"

    os.system(f"python scripts/run_tracker.py --is-obj-jointed {is_obj_jointed} \
                --dig-config-path {dig_config_path} \
                --video-path {test_video_path}/video.mp4 \
                --output-dir {outdir} \
                --no-save-hand")
    