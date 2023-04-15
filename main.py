import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
    
    Takes in a list of integers and runs a function on the integers to find the next largest prime number and returns a list of these next largest prime numbers.
    Args:
        List[int]: list of integers that are being passed to this function
    Returns:
        List[int]: list of integers of the next largest primes
    """

    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?

    Takes in a list of integers and runs a function on the integers to find the next largest prime number and returns a list of these next largest prime numbers.
    Args:
        List[int]: list of integers that are being passed to this function
    Returns:
        List[int]: list of integers of the next largest primes
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?

    Takes in two lists of integers which are then zipped and the difference is taken, the mean is calculated from the resulting differences.
    Args:
        List[int]: two of these are taken in
    Returns:
        List[int]: one list is returned from the two input lists
    """
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://127.0.0.1:5000' # TODO: Change this to the IP address of your server

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            p1=offload_url+'/process1'
            response = requests.post(p1,json=data)
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2 = None
        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            p2=offload_url+'/process2'
            response = requests.post(p2,json=data)
            data2 = response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
        pass
    elif offload == 'both':
        # TODO: Implement this case
        data1,data2 = None, None
        def offload_process1(data):
            nonlocal data1
            b = offload_url+'/both'
            response = requests.post(b,json=data)
            data1 = response.json()
        thread1 = threading.Thread(target=offload_process1, args=(data,))
        thread1.start()

        def offload_process2(data):
            nonlocal data2
            response = requests.post(offload_url,json=data)
            data2 = response.json()
        thread2 = threading.Thread(target=offload_process2, args=(data,))
        thread2.start()
        thread1.join()
        thread2.join()
        pass

    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
    offloading_modes=[None,'process1','process2','both']
    num_runs = 5

    results_df = pd.DataFrame(columns=['mode','time'])

    for mode in offloading_modes:
        total_time=0
        for i in range(num_runs):
            start_time = time.time()
            run(mode)
            end_time = time.time()
            elapsedtime = end_time - start_time
            total_time += elapsedtime
        meantime = total_time/num_runs
        std_time = pd.Series([time.time() - start_time for i in range(num_runs)]).std()
        results_df = results_df._append({'mode':mode, 'time':meantime}, ignore_index=True)


    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels
    plt.bar(x=results_df['mode'], height=results_df['time'], yerr=std_time)
    plt.title('Execution time by offloading mode')
    plt.xlabel('Offloading mode')
    plt.ylabel('Total execution time')
    plt.show()
    # TODO: save plot to "makespan.png"


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()
