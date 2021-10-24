X = [2.000,2.333,2.667,3.000]
Y = [30,40,68,80]
plt.scatter(X,Y)
plt.plot(X,Y)
plt.title("Position vs. Time on a Roadtrip")
plt.xlabel("Time (in hours)")
plt.ylabel("Odometer Reading (in miles)")
plt.show()



# SOLUTION - second (better) version
def approximate_derivative(f, t):
    # 1. Set delta_t. Note that I've made it REALLY small.
    delta_t = 0.00001
    
    # 2. calculate the vertical change of the function
    #    NOTE that the "window" is not centered on our 
    #    target time anymore. This shouldn't be a problem
    #    if delta_t is small enough.
    vertical_change = f(t + delta_t) - f(t)
    
    # 3. return the slope
    return vertical_change / delta_t

deriv_at_3_point_45 = approximate_derivative(position_b, 3.45)
print("The derivative at t = 3.45 is", deriv_at_3_point_45)




def integral(f, t1, t2, dt=0.1):
    # area begins at 0.0 
    area = 0.0
    
    # t starts at the lower bound of integration
    t = t1
    
    # integration continues until we reach upper bound
    while t < t2:
        
        # calculate the TINY bit of area associated with
        # this particular rectangle and add to total
        dA = f(t) * dt
        area += dA
        t += dt
    return area



def get_integral_from_data(acceleration_data, times):
    # 1. We will need to keep track of the total accumulated speed
    accumulated_speed = 0.0
    
    # 2. The next lines should look familiar from the derivative code
    last_time = times[0]
    speeds = []
    
    # 3. Once again, we lose some data because we have to start
    #    at i=1 instead of i=0.
    for i in range(1, len(times)):
        
        # 4. Get the numbers for this index i
        acceleration = acceleration_data[i]
        time = times[i]
        
        # 5. Calculate delta t
        delta_t = time - last_time
        
        # 6. This is an important step! This is where we approximate
        #    the area under the curve using a rectangle w/ width of
        #    delta_t.
        delta_v = acceleration * delta_t
        
        # 7. The actual speed now is whatever the speed was before
        #    plus the new change in speed.
        accumulated_speed += delta_v
        
        # 8. append to speeds and update last_time
        speeds.append(accumulated_speed)
        last_time = time
    return speeds

# 9. Now we use the function we just defined
integrated_speeds = get_integral_from_data(ACCELERATIONS, TIMESTAMPS)

# 10. Plot
plt.scatter(TIMESTAMPS[1:], integrated_speeds)
plt.show()
