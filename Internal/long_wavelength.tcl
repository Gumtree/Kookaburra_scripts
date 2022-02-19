#run bex 0 # can stay out of the beam 17.8.2017

run ss1u 16.96
run ss1d -32.3
run ss1l 2.75
run ss1r 53.35

run ss2u 27.5
run ss2d -27.5
run ss2l -27.5
run ss2r 27.5

run m1om 180.08
run m1x 0

#run mdet 19

drive samz 617 m2y 300 
# have changed m2y to 300 just to be safe with new changer

drive m2om 179.75
drive m2x -5.66
#drive m2y 0 # to do after check of sample position (knob)

wavelength 4.74