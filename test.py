import numpy as np
import time

# Function to create an .npz file with 100 parameters
def create_npz_file(file_path):
    params = {f'param{i}': i for i in range(10)}
    np.savez(file_path, **params)

# Function 1: Takes individual parameters and prints them
def function1(param0, param1, param2, param3, param4, param5, param6, param7, param8, param9):
    print(param0, param1, param2, param3, param4, param5, param6, param7, param8, param9)

# Function 2: Takes a parameters dictionary and prints them
def function2(params):
    print(params['param0'], params['param1'], params['param2'], params['param3'], params['param4'],
          params['param5'], params['param6'], params['param7'], params['param8'], params['param9'])

def main():
    loop_times = 10000
    file_path = 'params.npz'
    create_npz_file(file_path)
    
    # Load the parameters
    params_data = np.load(file_path)
    
    # Extract individual parameters
    params_list = [params_data[f'param{i}'] for i in range(10)]
    
    # Measure time for Function 1
    start_time = time.time()
    for _ in range(loop_times):
        function1(*params_list)
    end_time = time.time()
    func1_time = end_time - start_time
    
    # Measure time for Function 2
    start_time = time.time()
    for _ in range(loop_times):
        function2(params_data)
    end_time = time.time()
    print(f"Function 1 executed in {func1_time:.2f} seconds")
    print(f"Function 2 executed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
