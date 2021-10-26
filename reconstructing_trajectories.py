def get_speeds(data_list):
    time_list = [row[0] for row in data_list]
    dis_list = [row[1] for row in data_list]
    yaw_list = [row[2] for row in data_list]
    acc_list = [row[3] for row in data_list]
    
    accumulated_speed = 0.0
    last_time = time_list[0]
    last_disp = 0.0
    
    speeds = [0]
    
    
    for i in range(1, len(time_list)):
        #Version using odometer
        time = time_list[i]
        disp = dis_list[i]
        delta_times = time-last_time
        delta_disp = disp-last_disp
        speed = delta_disp/delta_times
        
        speeds.append(speed)
        last_time = time
        last_disp = disp
    
    '''
    #Version using accelerometer
    for i in range(1,len(time_list)):
        acceleration = acc_list[i]
        time = time_list[i]
        
        delta_times = time-last_time
        delta_v = acceleration * delta_times
        
        accumulated_speed = accumulated_speed + delta_v
        speeds.append(accumulated_speed)
        last_time = time
    '''
    return speeds
#Finished



#=============================Todo =============================
def get_headings(data_list):
    accum_theta = 0.0
    last_time = data_list[0][0]
    theta_list =list()
    theta_list.append(0)
    
    for i in range(len(data_list[0])):
        import math

        time = data_list[0][i]
        yaw = data_list[2][i]
        
        delta_times = time-last_time
        delta_theta = yaw*delta_times
        
        accum_theta = accum_theta + delta_theta
        accum_theta %= (2 * math.pi)
        theta_list.append(accum_theta)
    return theta_list

def get_x_y(data_list):
    import math
    
    thetas = get_headings(data_list)
    x=0
    y=0
    ans=[(x,y)]
    
    for i in range(len(data_list[0])):
        x=x+data_list[1][i]*math.cos(thetas[i])
        y=y+data_list[1][i]*math.sin(thetas[i])
        ans.append((x,y))    
    
    return ans

def show_x_y(data_list):
    XY = get_x_y(data_list)
    headings = get_headings(data_list)
    X  = [d[0] for d in XY]
    Y  = [d[1] for d in XY]
    h_x = np.cos(headings)
    h_y = np.sin(headings)
    Q = plt.quiver(X[::increment],
                   Y[::increment],
                   h_x[::increment],
                   h_y[::increment],
                   units='x',
                   pivot='tip')
    qk = plt.quiverkey(Q, 0.9, 0.9, 2, r'$1 \frac{m}{s}',
                       labelpos='E', coordinates='figure')
    plt.show()
