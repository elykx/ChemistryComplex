def change_exp_data(experimental_data, solution, time):
    exp_point = experimental_data.copy()
    for i in range(len(time)):
        for j in range(len(experimental_data)):
            if experimental_data[j][0] == time[i]:
                print(solution[i])
                exp_point[j][1:] = solution[i]
    return exp_point
