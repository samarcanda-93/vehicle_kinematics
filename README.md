# TODO: Update README

1. Parse the GPS data input into a data structure. Dataclass, tuple, namedtuple.
2. Build a list with those records.
3. Build a projector of the post on the xy space
4. Calculate velocity vector (moving direction)

## Assumptions

- x_mm, y_mm coordinates are the GNSS module position in a **fixed** 2D world frame of
  reference.
- The vehicle moves forward smoothly
- The GNSS module is mounted on a rigid post and remains constantly at h= 1500[mm]
  height above moving plain, meaning that The post does not bend, flex, or vibrate
  significantly.
- The post is constantly perpendicular to the moving plane, and its base lies in the
  moving plane.
- The vehicle body can be approximated locally as a rigid moving plane. This means that
  GNSS module is low enough to see the robot as a plane. Similar to the f = mg flat
  earth approximation concept.
- roll_deg describes lateral tilt of the vehicle.
- Positive roll means the right side of the vehicle is lower than the left side.
- pitch_deg describes longitudinal tilt of the vehicle.
- Positive pitch means the front of the vehicle is lower than the rear.
- Roll and pitch are accurate and synchronized with the GNSS position timestamps (no transmission delay)
- The terrain may be rugged, but the motion is smooth enough that heading estimation
  from neighboring samples is meaningful.
- We solve the problem in 2D world coordinates plus attitude angles, without modeling
  full 3D terrain geometry beyond the local moving plane. The vehicle is modeled as a
  rigid body with a single local moving plane. The local terrain/support plane is
  assumed to coincide with the vehicle moving plane at each time.
- Movement is smooth, so that calculated velocity (heading) and gps data are coherent
- generate a 2D trajectory plot comparing raw GNSS positions with projected post-foot
  positions, a heading-over-time plot, a roll/pitch-over-time plot, and optionally a
  small animation of the moving plane, antenna post, and projected point. colormaps
  seems cool here.
- heading is computed from the direction of the planar velocity vector
  this assumes motion direction aligns with vehicle heading
