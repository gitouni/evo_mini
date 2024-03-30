import os
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from evo.tools import file_interface
from evo.core.trajectory import PoseTrajectory3D
from evo.core import sync
import argparse


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ax_label_fontsize", type=int, default=15)
    parser.add_argument("--ax_legend_fontsize", type=int, default=16)
    parser.add_argument("--kitti_dirs", type=str, nargs="+", default=['09_4','08_4'])
    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    parameters = {"xtick.labelsize": args.ax_label_fontsize,
                  "ytick.labelsize": args.ax_label_fontsize,
                  "legend.fontsize": args.ax_legend_fontsize}
    plt.rcParams.update(parameters)
    file2label = dict(GT="GT", VLO="VLO", VINSMono="VINS-Mono",VILO="VILO",liosam="LIO-SAM")
    marks = dict(GT="k-", VLO="y-.", VINSMono="r--",VILO="b-.",liosam="g--")

    for directory in args.kitti_dirs:
        files = list(sorted(os.listdir(directory)))
        plt.figure()
        for file in files:
            name = os.path.splitext(file)[0]
            filename = os.path.join(directory, file)
            label = file2label[name]
            traj: PoseTrajectory3D = file_interface.read_tum_trajectory_file(filename)
            if name == "GT":
                ref_traj = traj

    for directory in args.kitti_dirs:
        files = list(sorted(os.listdir(directory)))
        plt.figure()
        for file in files:
            name = os.path.splitext(file)[0]
            filename = os.path.join(directory, file)
            label = file2label[name]
            traj: PoseTrajectory3D = file_interface.read_tum_trajectory_file(filename)
            if name == "GT":
                ref_traj = traj
            else:
                ref_traj, traj = sync.associate_trajectories(ref_traj, traj)
                traj.align(ref_traj)
            x = traj.positions_xyz[:, 0]  # x
            y = traj.positions_xyz[:, 2]  # z
            # plt.xlim(0,1000)
            # plt.ylim(0,1000)
            plt.plot(x, y, marks[name], label=label)
        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0fm'))
        plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0fm'))
        plt.tight_layout()
        plt.legend(loc='best')
        plt.savefig("kitti_{}.png".format(directory))