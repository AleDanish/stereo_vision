# stereo_vision

Fixed window and variable window stereo vision algorithms implementation for dense 3D reconstruction.

* Algorithms can be executing by typing:

``python variable_window.py -f 3 -w all``


* Parameters:

-f | --filter_size : indicate the size of the patch. Default value: 3. Values allowed: 3, 5, 7, 9.

-w | -- window_type : indicate the type of execution. Default: all. Values allowed::
   `all` - fixed and variable window algorithms execution
   `fixed` - fixed window algorithm execution
   `variable` - variable window algorithm execution
   `disparity` - shows only the disparity map
