import os
import yaml
import glob


with open("partnet_mobility_data_split.yaml", "r") as f:
    data_config = yaml.safe_load(f)
test_video_list = data_config["test"]
for test_video_path in test_video_list:
    # may need to modify the scan data path
    test_scan_path = test_video_path[:test_video_path.rfind("view_")] + "view_init_rsrd/"
    os.system(f"ns-train garfield --data {test_scan_path}")

    outdir = f"outputs/{test_scan_path}"
    garfield_path = f"{outdir}/garfield/"
    garfield_config_path_list = glob.glob(f"{garfield_path}/*/config.yml")
    assert len(garfield_config_path_list) > 0, "no garfield config found"
    garfield_config_path = garfield_config_path_list[-1]
    os.system(f"ns-train dig --data {test_scan_path} --pipeline.garfield-ckpt {garfield_config_path}")
