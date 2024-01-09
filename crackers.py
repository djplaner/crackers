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

Streamlit app implementing basic Crackers game

Game will progress through the following stages

1. Welcome 
    - display information about the game
    - Allow choice of how big a number range to use
    - Allow user to chose from 31, 63 where the number equals 2^n - 1
      Where n will be the number of times user asked "Is your number here"
2. Is your number here 
    - happens n times
    - present user with a list of numbers based on n
    - user selects yes/no for each list
    - before the next list is displayed
3. Is this your number
    - The calculated number is displayed
"""

import streamlit as st 

import pandas as pd

#from crackers import generateCrackersNumbers

placeholder = st.empty()

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

#    st.write(f"n: {n} maxN: {maxN}")
    # Loop through all numbers from 2^(n-1) to 2^maxN - 1
    # If the number has the n bit set, add it to the list
    for i in range( int(2**(n)), int(2**(maxN)) ) :
        if ( i & 2**(n) ) :
            numbers.append( i )

    return numbers

def convertNumbersToMarkdown( numbers : list ) -> str :
    """
    Given a list of numbers convert them to a markdown table with 8 columns
    and return a string with that markdown

    Kludge

    """

    markdown = """
|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""
    count = 0
    for number in numbers:
        if count == 0:
            markdown += "| "
        markdown += str(number) + " | "
        count += 1
        if count == 8:
            markdown += "\n"
            count = 0 

    return markdown
    

#-------------------
# Define the game stage pages

def welcome():
    """
    Display a welcome message
    """
    st.title("Can I read your mind??!!! Let's see...")

    st.markdown("""
1. Pick any number between 1 and 63 - but don't tell me!!!
2. Answer 6 simple questions.
3. I will read your mind and tell you what number you picked. 
""")

    st.button("Start!!", on_click=nextStage)

def nextStage(numPresent: bool = False):
    """
    Move onto the next stage.
    
    If numPresent that means the gameStage represents a value of n where 2^(n-1) is one of the numbers that adds up to the number the user is thinking of.
    """
    st.session_state['gameStage'] += 1

    placeholder.empty()
    
def nextStageAddition():

    st.session_state['myGuess'] += 2**(st.session_state['gameStage'] - 1)
    st.session_state['gameStage'] += 1
    placeholder.empty()

def isYourNumberHere():
    st.title("Is your number in the table below?")

    col1, col2, col3 = st.columns(3)
    with col1:
        button1 = st.button("Yes", on_click=nextStageAddition)

    with col2:
        button2 = st.button("No", on_click=nextStage)

    with col3:
        button3 = st.button("Start again", on_click=startAgain)

    numbers = generateCrackersNumbers( st.session_state['gameStage']-1, st.session_state['maxN'] )
    numbersMarkdown = convertNumbersToMarkdown( numbers )

    #-- convert numbers list to a 8 column data frame 
    #   and display it
    st.markdown( numbersMarkdown )

def startAgain():
    for name in 'gameStage', 'maxN':
        del st.session_state[name]

def isThisYourNumber():
    st.title(f"Is {st.session_state['myGuess']} your number?")

    st.button("Start again", on_click=startAgain)

#-- Set up the variables

if 'gameStage' not in st.session_state:
    st.session_state['gameStage'] = 0

if 'myGuess' not in st.session_state:
    st.session_state['myGuess'] = 0

if 'maxN' not in st.session_state:
    st.session_state['maxN'] = 6

gameStageFunctions = [
    welcome, isYourNumberHere, isThisYourNumber
]

if st.session_state['gameStage'] == 0:
    st.session_state['myGuess'] = 0
    welcome()
elif st.session_state['gameStage'] <= st.session_state['maxN']:
    isYourNumberHere()
elif st.session_state['gameStage'] > st.session_state['maxN']:
    isThisYourNumber()





