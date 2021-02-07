motor_name = 'samz'
motor_limits = [28, 630]
no_of_runs = 100
sleep_between_runs = 5

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
        except:
            slog('failed')
            f += 1
        time.sleep(sleep_between_runs)
    slog('The test is finished with {} success and {} fails'.format(s, f))
        
    