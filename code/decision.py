import numpy as np

def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check mode. Forward, stopMode=forward?
        if Rover.mode == 'forward':
            # Check if navigable terrain
            if (len(Rover.nav_angles) >= Rover.stop_forward) and \
                 (np.mean(Rover.nav_dists > 20)):
                # If Forward and navigable terrain, then throttle
                if (Rover.vel < Rover.max_vel) and (Rover.steer < 5):
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.throttle = Rover.throttle_set
                else: # Reduce throttle
                    Rover.throttle = 0
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # If not navigable terrain pixels then stop
            elif (len(Rover.nav_angles) < Rover.stop_forward) or \
                 (np.mean(Rover.nav_dists < 20)):
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'stop'

        # # Mode=stop?
        elif Rover.mode == 'stop':
            # If still moving keep braking
            if Rover.vel > 0.5:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If not moving then do...
            elif Rover.vel <= 0.5:
                # If no path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    Rover.brake = 0
                    Rover.steer = -15
                # If stopped and navigable terrain in: forward
                if len(Rover.nav_angles) >= Rover.go_forward:
                    Rover.throttle = Rover.throttle_set
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
        # If sample detected
        elif Rover.mode == 'goto_rock':
            # if sample picked up, exit mode
            if Rover.picking_up:
                Rover.mode = 'stop'
            else:
                # if the rover can pick up sample, stop and pick it up
                if Rover.near_sample:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                # Still moving, start to brake
                elif Rover.vel > np.mean(Rover.nav_dists):
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set/2
                # Still too far away, keep going
                elif Rover.vel < Rover.max_vel/2:
                    Rover.throttle = Rover.throttle_set/2
                    Rover.brake = 0
                # Too fast, brake
                elif Rover.vel > Rover.max_vel/2:
                    Rover.throttle = 0
                    Rover.brake = Rover.throttle_set/3

    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        # Enter mode 'stop' after picking up
        Rover.mode = 'stop'

    return Rover
