import time
from fit_inp import fit_inp
from input_parameters import input_parameters
from fit_run import fit_run

def main():
    analysis_dir = "./test/"
    
    # Start the timer
    start_time = time.time()
    
    # fit_inp(analysis_dir)
    input_parameters(analysis_dir)
    fit_run(analysis_dir)
    
    # Stop the timer
    end_time = time.time()
    
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Program executed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
