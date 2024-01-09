# Copyright (C) 2024 David Jones
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
crackers.py

Library for basic functions associated with implementing the game/task "Crackers" (see https://www.youcubed.org/tasks/crackers/).

"""

def generateCrackersNumbers( n : int = 1, maxN : int = 7 ) -> list :
    """
    Generate a list of numbers that represent the numbers on the nth card in a sequence that contains maxN cards.

    Each card will contain a list of numbers that are all the numbers between 2^(n-1) and 2^(maxN-1) - 1 that have the n bit set to 1 (when the number is represented as a binary number)
    
    Parameters
    ----------
    n: defines the minimum number on the card 2^(n-1)
    maxN: defines the maximum number of bits in the allowed binary numbers 2^maxN - 1
    """

    numbers = []

    # Loop through all numbers from 2^(n-1) to 2^maxN - 1
    # If the number has the n bit set, add it to the list
    for i in range( 2**(n-1), 2**(maxN) ) :
        if ( i & 2**(n-1) ) :
            numbers.append( i )

    return numbers





if __name__ == "__main__":

    for i in range( 1, 7 ) :
        print( "n = ", i, ":", generateCrackersNumbers( i, 6 ) )
        print()



