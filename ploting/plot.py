import matplotlib.pyplot as plt

def plot1D(data):
    # Plotting the values
    plt.plot(data, marker='o')

    # Adding title and labels
    plt.title('Plot of Given Values')
    plt.xlabel('Index')
    plt.ylabel('Value')

    # Display the plot
    plt.show()
