import os
import yaml
import glob


with open("partnet_mobility_data_split.yaml", "r") as f:
    data_config = yaml.safe_load(f)
test_video_list = data_config["test"]
# test_video_list = ["sim_data/partnet_mobility/Scissors/10973/joint_0_bg/view_1/",
#                    "sim_data/partnet_mobility/Refrigerator/10867/joint_0_bg/view_1/",
#                    "sim_data/partnet_mobility/USB/100072/joint_0_bg/view_0/",]
# obj_id_list = ["10867", "10973", "100072"]
obj_id_list = []
for test_video_path in test_video_list:
    # may need to modify the scan data path
    obj_id = test_video_path.split('/')[3]
    if obj_id in obj_id_list:
        continue
    obj_id_list.append(obj_id)
    test_scan_path = "data/" + test_video_path[test_video_path.find("partnet"):test_video_path.rfind("view_")] + "view_init_rsrd/"
    outdir = f"outputs/" + test_video_path[test_video_path.find("partnet"):test_video_path.rfind("view_")]
    garfield_path = f"{outdir}/view_init_rsrd/garfield/"
    if not os.path.exists(garfield_path):
        os.system(f"ns-train garfield --data {test_scan_path} --output-dir {outdir} --experiment-name view_init_rsrd --viewer.quit-on-train-completion True")

    garfield_config_path_list = glob.glob(f"{garfield_path}/*/config.yml")
    if len(garfield_config_path_list) == 0:
        continue
    garfield_config_path = garfield_config_path_list[-1]
    dig_path = f"{outdir}/view_init_rsrd/dig/"
    if not os.path.exists(dig_path):
        os.system(f"ns-train dig --data {test_scan_path} --pipeline.garfield-ckpt {garfield_config_path} --output-dir {outdir} --experiment-name view_init_rsrd \
                --viewer.quit-on-train-completion True")
    
    # if os.path.exists(f"{outdir}/view_init_rsrd/state.pt"):
    #     continue
    # print(dig_path)
    # dig_config_path_list = glob.glob(f"{dig_path}/*/config.yml")
    # dig_config_path_list.sort()
    # if len(dig_config_path_list) == 0:
    #     continue
    # dig_config_path = dig_config_path_list[-1]
    # os.system(f"ns-viewer --load-config {dig_config_path} --viewer.websocket-host 127.0.0.1")