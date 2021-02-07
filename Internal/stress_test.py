from org.gumtree.gumnix.sics.io import SicsExecutionException
'''
 Below is a script to test driving a motor to a random value in 
 certain range for a defined number of times. 
 
 Parameters:
     motor_name : name of the motor to be tested
     
     motor_limits : the lower and upper limits of the motor range
     
     no_of_runs : number of runs in the test
     
     sleep_between_runs : wait for certain time between each run
     
''' 
motor_name = 'samz'
motor_limits = [28, 630]
no_of_runs = 100
sleep_between_runs = 5

# below parameters for debugging purpose, please don't change them
#motor_name = 'dummy_motor'
#motor_limits = [0, 100]
#no_of_runs = 5

def run():
    s = 0
    f = 0
    pos = rand([no_of_runs]) * (motor_limits[1] - motor_limits[0]) + motor_limits[0]
    for i in xrange(no_of_runs):
        slog('test number {}'.format(i + 1))
        slog('drive {} {}'.format(motor_name, pos[i]))
        try:
            sics.drive(motor_name, pos[i])
            slog('successful')
            s += 1
        except SicsExecutionException, ex:
            slog('interrupted')
            slog('The test is interrupted with {} success and {} fails'.format(s, f))
            raise
        except:
            slog('failed')
            f += 1
        time.sleep(sleep_between_runs)
    slog('The test is finished with {} success and {} fails'.format(s, f))
        
run()