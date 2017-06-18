## Project: Search and Sample Return

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook).
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands.
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg
[image4]: ./rover_decicion_tree.png
[image5]: ./processed_images.png
[image6]: ./processed_video_sample.png

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

The main functions required to solve this section was a threshold function and a warp function. For the obstacle part, it was enough to run a single threshold function with a threshold set to 160 for all three color channels. Reverse of this solved the drivable area problem as well. For the rock samples the thresholds was a bit more sophisticated with both an upper bound and a lower bound. The thresholds for rock samples look like this:
* 130 < Red < 205
* 100 < Green < 180
* 0 < Blue < 60

##### Samples of processed images
![alt text][image5]

#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result.

I populated the steps below the TODO section to process each image and generate a movie in the end. The steps to be populated was:
* Define source and destination points for perspective transform
* Apply perspective transform
* Apply color threshold to identify navigable
* warped image to world coordinates
* Update worldmap (to be displayed on right side of screen)
* Make a mosaic image, below is some example code

The video from the processing steps can be found here: [output/test_mapping.mp4](./output/test_mapping.mp4)

##### Snapshot from the finalmovie
![alt text][image6]

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

##### Perception
I used the code from the notebook as a starting point, and filled in code for the suggested steps to provide perception for the Rover.
1. Define source and destination points for perspective transform
2. Apply perspective transform
3. Apply color threshold to identify navigable terrain/obstacles/rock samples
4. Update Rover.vision_image (this will be displayed on left side of screen)
5. Convert map image pixel values to rover-centric coords
6. Convert rover-centric pixel values to world coordinates
7. Update Rover worldmap (to be displayed on right side of screen)
8. Convert rover-centric pixel positions to polar coordinates

##### Decision
The implementer decicion tree looks like this:
![alt text][image4]

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

I ran the simulator at resolution 1440x900 with detail level 'Good'.

In autonomous drive I normally get around 20 FPS.
Most of the time the Rover can drive the whole map without any issues, but it sometimes get stuck in the big open area driving in circles. It is also very bad at picking up the samples. I think the stop procedure is the main reason for this.

The Rover could benefit from favouring unexplored areas of the map instead of the current random drive.
