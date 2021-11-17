class Solution(object):
    def containsDuplicate(self, nums):
        num_dict = {} # Empty Dictionary 
        for num in nums: # Iterates through array of given nums
            if num not in num_dict: # If num value not in dictionary, add it.
                num_dict[num] = 1
            else: # Else, Num has been added to dictionary before, return True
                return True
        return False
        




""" 
Given an integer array nums, return true if any value appears at least twice 
in the array, and return false if every element is distinct.

"""