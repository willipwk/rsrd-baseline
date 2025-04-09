import numpy as np
import open3d as o3d
import cv2
import json
import os
import glob


intrinsics_path = "data/partnet_mobility/Table/23372/joint_1_bg/view_1/intrinsics.npy" # all the intrinsics are the same
intrinsics = np.load(intrinsics_path)
fl_x = float(intrinsics[0, 0])
fl_y = float(intrinsics[1, 1])
cx = float(intrinsics[0, 2])
cy = float(intrinsics[1, 2])
w = 640
h = 480
# sapien_scan_dir = glob.glob("path/to/view_init_rsrd")
sapien_scan_dir = glob.glob("data/partnet_mobility/*/*/joint_[0-9]_bg/view_init_rsrd")
for sapien_scan in sapien_scan_dir:
    # init pc
    surface_img = []
    surface_xyz = []
    rgb_dir = f"{sapien_scan}/rgb"
    rgb_len = len(os.listdir(rgb_dir))
    for i in range(rgb_len):
        img = cv2.imread("{}/rgb/{}".format(sapien_scan, "%06d.png" % i))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        surface_img.append(img)
        xyz = np.load("{}/xyz/{}".format(sapien_scan, "%06d.npz" % i))['a']
        surface_xyz.append(xyz)
    surface_rgb = np.stack(surface_img).reshape(-1, 3)
    surface_xyz = np.stack(surface_xyz).reshape(-1, 3)

    sample_num = min(480 * 64, surface_rgb.shape[0])
    sample_index = np.random.choice(np.arange(surface_rgb.shape[0]), sample_num, replace=False)
    surface_pcd = o3d.geometry.PointCloud()
    surface_pcd.points = o3d.utility.Vector3dVector(surface_xyz[sample_index])
    surface_pcd.colors = o3d.utility.Vector3dVector(surface_rgb[sample_index] / 255.)
    o3d.io.write_point_cloud(f"{sapien_scan}/point_cloud.ply", surface_pcd)

    camera_dir = f"{sapien_scan}/camera"
    camera_pose_list = os.listdir(camera_dir)
    camera_pose_list.sort()
    transforms_dict = {"camera_model": "OPENCV", "orientation_override": "none", "frames": [], "ply_file_path": "point_cloud.ply"}
    # print(intrinsics)
    for frame_id, camera_pose_path in enumerate(camera_pose_list):
        camera_pose = np.load(f"{camera_dir}/{camera_pose_path}")['a']
        # print(camera_pose)
        # opencv_pose = camera_pose * np.array([[1, -1, -1, 1]])
        # print(opencv_pose)
        file_path = "./rgb/%06d.png" % (frame_id)
        # print(file_path)
        # print(opencv_pose.tolist())
        frame_dict = {"fl_x": fl_x, "fl_y": fl_y, "cx": cx, "cy": cy, "w": w, "h": h, "file_path": file_path,
                    "transform_matrix": camera_pose.tolist()}
        transforms_dict["frames"].append(frame_dict)
    with open(f"{sapien_scan}/transforms.json", "w") as f:
        json.dump(transforms_dict, f)
