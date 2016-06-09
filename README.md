# stereo_vision

Fixed window and variable window stereo vision algorithms implementation for dense 3D reconstruction.

Parameters:

-f | --filter_size	->	indicate the size of the patch. Values allowed: 3, 5, 7, 9. Default value: 3.

-w | -- window_type	->	indicate the type of execution. Values allowed: all, fixed, variable, disparity. Default: all.
* `all`_ - fixed and variable window algorithms execution
* `fixed`_ - fixed window algorithm execution
* `variable`_ - variable window algorithm execution
* `disparity`_ - shows only the disparity map
