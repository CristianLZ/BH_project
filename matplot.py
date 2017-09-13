# setting the library as a variable called plt
import matplotlib.pyplot as plt


squares = [1,4,9,16,25]

# plotting the data
plt.plot(squares)
# setting the title of the graph
plt.title("Square numbers", fontsize=14)
plt.xlabel("Value X")
plt.ylabel("Value Y")
plt.show()

