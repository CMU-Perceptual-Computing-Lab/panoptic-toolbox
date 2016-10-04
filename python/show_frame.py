'''
This example projects skeletons onto a camera and writes the resulting image, e.g.,

python show_frame.py ../sampleData/ 1 1 0

will project skeletons on camera with panel 1, node 1, ("01_01") and frame number 0,
producing a file sampleData_01_01_00000000.jpg

This software is provided for research purposes only.
More information here: http://domedb.perception.cs.cmu.edu
'''

import argparse
import os
import numpy as np
import json
import cv2

# Edges in the skeleton
edges = np.array([[1,2],[1,4],[4,5],[5,6],[1,3],[3,7],[7,8],[8,9],[3,13],[13,14],[14,15],[1,10],[10,11],[11,12]])-1

# Random colors to draw skeletons
colors = np.random.randint(50,256,(100,3))

def load_cameras( data_path, seq_name ):
    """Load the camera calibration file for a given sequence"""

    # Load camera calibration file
    with open(data_path+'/calibration_{0}.json'.format(seq_name)) as cfile:
        calib = json.load(cfile)

    # Cameras are identified by a tuple of (panel#,node#)
    cameras = {(cam['panel'],cam['node']):cam for cam in calib['cameras']}

    # Convert data into numpy arrays for convenience
    for k,cam in cameras.iteritems():
        cam['K'] = np.matrix(cam['K'])
        cam['distCoef'] = np.array(cam['distCoef'])
        cam['R'] = np.matrix(cam['R'])
        cam['t'] = np.array(cam['t']).reshape((3,1))

    return cameras

def load_image( data_path, panel, node, frame_index ):
    """Load an image given a camera name and frame number"""

    prefix = "hd" if panel==0 else "vga"
    img_path = data_path+'/{0}Imgs/'.format(prefix)
    img_fname = img_path+'{0:02d}_{1:02d}/{0:02d}_{1:02d}_{2:08d}.jpg'.format(panel, node, frame_index)

    im = cv2.imread(img_fname)
    if im is None:
        print('Image file not found: {0}'.format(img_fname))
        exit(1)
    return im

def load_skeletons( data_path, panel, frame_index ):
    """Load skeletons given a panel and frame number"""

    # HD and VGA frames are indexed differently
    prefix = "hd" if panel==0 else "vga"
    skel_json_path = data_path+'/{0}Pose3d_stage1/'.format(prefix)

    bframe = { "bodies": [] }
    skel_json_fname = skel_json_path+'body3DScene_{0:08d}.json'.format(frame_index)
    try:
        with open(skel_json_fname) as fid:
            bframe = json.load( fid )

    except IOError as e:
        print('Error reading skeletons {0}\n'.format(skel_json_fname)+e.strerror)
        print('No skeletons available')

    return bframe

def draw_skeletons( im, bframe, cam ):
    """Plot skeletons onto image"""

    for body in bframe['bodies']:
        if body['id']<0:
            # This is an outlier.
            continue

        skel = np.array(body['joints15']).reshape((-1,4)).transpose()

        # Project skeleton into view
        pt = cv2.projectPoints(skel[0:3,:].transpose().copy(),
                      cv2.Rodrigues(cam['R'])[0], cam['t'], cam['K'],
                      cam['distCoef'])

        pt = np.squeeze(pt[0], axis=1).transpose()

        # Show only points detected with confidence
        valid = skel[3,:]>0.1

        # Plot edges for each bone
        col = tuple(colors[body['id']])
        for edge in edges:
            if valid[edge[0]] or valid[edge[1]]:
                cv2.line(im,
                tuple(pt[0:2,edge[0]].astype(int)),
                tuple(pt[0:2,edge[1]].astype(int)), col, 2)

def main():
    parser = argparse.ArgumentParser(description="Show a frame with overlaid skeletons.")
    parser.add_argument('data_path', type=str)
    parser.add_argument('panel', type=int)
    parser.add_argument('node', type=int)
    parser.add_argument('frame', type=int)
    parser.add_argument('--outputfile', type=str, nargs='?', default=None)
    args = parser.parse_args()

    data_path = args.data_path
    panel = args.panel
    node = args.node
    frame = args.frame
    outputfile = args.outputfile

    seq_name = os.path.basename(os.path.normpath(data_path))

    if panel<0 or panel>20:
        print('Panel {0} not yet supported'.format(panel))
        exit(1)

    cameras = load_cameras(data_path, seq_name)

    im = load_image(data_path, panel, node, frame)
    bframe = load_skeletons(data_path, panel, frame)

    draw_skeletons(im, bframe, cameras[(panel,node)])

    if outputfile is None:
        outputfile = '{3}_{0:02d}_{1:02d}_{2:08d}.jpg'.format(panel,node,frame,seq_name)
    print('Writing {0}'.format(outputfile))
    cv2.imwrite(outputfile, im)

if __name__=='__main__':
    main()
