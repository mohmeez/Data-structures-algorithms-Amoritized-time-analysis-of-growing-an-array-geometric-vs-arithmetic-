import matplotlib.pyplot as plt
import time

"""Instructions: Please change the first parameter of n on lines 176 and 181 to visualize the time cost plots of linear,
 and geometric resizing. Running the script will save the time cost plots of appending elements of size n as JPEG,
 files in the same working folder directory. These plots have been attached in the project submission folder."""


class DynamicArray:

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # count actual elements
        self._capacity = 1  # default array capacity
        self._A = self._make_array(self._capacity)  # low-level array
        self.cost = []  # Cost variable that accumulates cyber dollars for every append call to our object


    def _get_capacity(self):
        return self._capacity

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def _resize(self, c):  # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array
        self._capacity = c

    def __getitem__(self, k):
        """Return element at index k."""

        if 0 <= k < self._n:
            return self._A[k]
        elif k < 0 and self._n + k >= 0:
            return self._A[(self._n + k)]
        else:
            raise IndexError("Index out of bounds!")

    def _make_array(self, c):
        """Return new array with capacity c."""
        return [None] * c # override the ctype array from the original code fragment

    def __str__(self):
        """ Return a string representation of the array """

        result = "The array holds the following elements: " + ' '.join(str(i) for i in self._A)
        return result

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value (or raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item
                return  # exit immediately
        raise ValueError('value not found')  # only reached if no match

    def append(self, obj, ty):
        """
        :param obj: the element that gets appended to the dynamic array
        :param ty: a lower case string parameter specifies if the array grows linear by a constant of n + 10 or,
         geometric by size 2n where n is the current capacity of the array. accepts 'l' --> linear or 'g' --> geometric
        """

        if self._n == self._capacity:  # not enough room ---> resize the array by growing it

            if ty.lower() == 'g':  # If ty is g do geometric resizing
                geometric_cost = 2 * self._capacity  # when array is full, cost of append increases by 2 * array's capacity
                self._resize(2 * self._capacity)  #  double the capacity of the array
                self.cost.append(geometric_cost)   # append the cost of growing the array to the total cost variable

            elif ty.lower() == 'l':   # if ty is equal to 'l' proceed with linear resizing
                linear_cost = self._capacity + 10   #the cost of growing the array is the current capacity + a constant number 10
                self._resize(self._capacity + 10)   # resize the current array by its size + a constant number 10
                self.cost.append(linear_cost)   # Append the cost of linear resizing to the total cost variable

        incremental_cost = 1    # if the array doesn't require resizing, the cost of appending each element is 1 cyber dollar
        self.cost.append(incremental_cost)  # append the cost of individual appends to cost
        self._A[self._n] = obj  #assign the elemnts to the bigger array
        self._n += 1   # increase the size by 1

    def time_cost_linear(self, n, obj):
        """
        :param n: grow the array by appending n number of elements in range n
        :param obj: An object of class DynamicArray to grow and append to
        :return: time cost plots of amortized plots for linear resizing and rationalization
        """
        elapsed = []   # A list to hold the time it takes to append elements
        for i in range(n):  # iterate n times
            start = time.time_ns()   # initiate the time and start recording the time
            obj.append(i, 'l')       # append each item in range n to the object array using linear resizing
            finish = time.time_ns()  # time it takes to finish appending
            total_time = finish - start # calculate the elapsed time
            elapsed.append(total_time)  #append each time to the elapsed list
        plt.plot(elapsed, obj.cost[:len(elapsed)])   #plot the elapsed time vs the total cost for linear resizing,
        # (includes individual appends that dont require resizing)

        plt.xlabel("Time in Nano Seconds")    # declaring the x label
        plt.ylabel("Linear Cost Amortized Array")    #declaring the y label
        plt.title("Time VS Linear cost")    #declaring he title of the graph
        plt.savefig("Time VS Linear.jpg")    #save the resulting figure in the working file directory
        plt.show()   # show the graph
        plt.plot(obj.cost, color='red')   # plotting the linear cost on its own
        # plt.bar(list(range(1, len(obj.cost) + 1)), obj.cost)
        plt.xlabel('number of elements')
        plt.ylabel('cost per element')
        plt.title('Graph of Linear amortized cost!')
        plt.savefig("Linear_Cost_per_element.jpg")
        plt.show()
        linear_cost = round(sum(obj.cost), 2)
        linear_cost_amortized_avg = round((linear_cost / len(obj.cost)), 2)  # calculating the average cost of each
        # append operation
        # Rationalization:
        print(f"Rationaliztion for linear:\nThe amortized cost of growing the array linearly to size {n} is: {linear_cost_amortized_avg} cyber $ for each element!") # rationalizing the proposition 5.1  & 5.2 from chapter 5
        print(f"The total cost of growing the array for {n} elements in a linear amortized manner is {linear_cost} cyber $!")
        print(f"The cost of appending elements in a linear aysmptotic manner for upto hundred elements(for "
              f"simplicity) are:\n{obj.cost[:101]}")
        print()

    def time_cost_geometric(self, n, obj):  # The time cost function that calculates time and plots it against
        """
        :param n: grow the array by appending n number of elements in range n
        :param obj: An object of class DynamicArray to grow and append to
        :return: time cost plots of amortized plots for geometric resizing and rationalization
        """

        elapsed = []  # a list that holds the elapsed time
        for i in range(n):  # iterate n times
            start = time.time_ns()  # initiate the time and start recording the time
            obj.append(i, 'g') # append each item in range n to the object array using geometric resizing
            finish = time.time_ns()  # time it takes to finish appending
            total_time = finish - start  # calculate the elapsed time
            elapsed.append(total_time)  # append each time to the elapsed list
        plt.plot(elapsed, obj.cost[:len(elapsed)])  # plot the elapsed time vs the total cost for geometric resizing,
        # (includes individual appends that dont require resizing)

        plt.xlabel("Time in Nano Seconds")  # x label
        plt.ylabel("Geometric Cost Amortized Array")
        plt.title("Time VS Geometric cost")
        plt.savefig("Time vs geometric.jpg") # save the figure as a jpeg file in the working folder directory
        plt.show()  # show the graph
        plt.plot(obj.cost, color='red')  # plotting the geometric cost on its own
        plt.xlabel('number of elements')
        plt.ylabel('cost per element')
        plt.title('Graph of geometric amortized cost!')
        plt.savefig("Geometric_Cost_per_element.jpg")
        plt.show()
        geometric_cost = round(sum(obj.cost), 2)
        geometric_cost_amortized_avg = round((geometric_cost / len(obj.cost)),2)
        # Rationalization:
        print(f"Rationaliztion for geometric:\nThe amortized cost of growing the array geometrically to size {n} is: {geometric_cost_amortized_avg} cyber $ for each element!")  # rationalizing the proposition 5.1  & 5.2 from chapter 5
        print(f"The total cost of growing the array for {n} elements in a geometric amortized manner is {geometric_cost} cyber $!")
        print(f"The cost of appending elements in a geometric aysmptotic manner for upto hundred elements(for "
              f"simplicity) are:\n{obj.cost[:101]}")  # printing the total costs for each append operation,
        # we can traverse all by removing the slicing


if __name__ == '__main__':
    linear_array = DynamicArray()  # creating an object of DynamicArray class
    linear_array.time_cost_linear(10000, linear_array)  # calculating the linear time amortized cost for appending n,
    # elements. Please change the n to visualize the plots for appending smaller or larger appends. The code will save,
    # files in the working directory

    geometric_array = DynamicArray() # Creating an object of DynamicArray class
    geometric_array.time_cost_geometric(10000, geometric_array)  # calculating the geometric time amortized cost for appending n,
    # elements. Please change the n to visualize the plots for appending smaller or larger appends. The code will save plot,
    # files in jpeg format in the working directory.

    print()

    #Amortized aanalysis
    print("We can see that that growing an array geometrically is better in terms of time.\n"
          "We can see that appending each element costs us 1 cyber $ unless appending the element requires resizing.\n"
          "Geometric resizing involves doubling the capacity of our array allowing cheaper append operations for each expensive append that requires resizing.\n"
          "In geometric resizing, the total amount of cyber dollars spent for any computation will be proportional to the total time spent.\n"
          "As a result, the amortized running time of each append operation is BigO(1) and the amortized running time of n append operations is BigO(n).\n"
          "\nOn the other hand, growing the array linearly by a constant number takes a running time of theta(n^2).\n"
          "As a result, the overall cost remains quadratic.\nTherefore, if we are given a choice between quadratic and linear,\n"
          "choosing to grow the array geometrically by a size of 2n works better in the amortized cost time analysis.")
