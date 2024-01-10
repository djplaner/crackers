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

st.set_page_config(
    page_title="Play Crackers",
    page_icon=":tada:"
)

#-- help me debug my understanding of program execution in Streamlit
DEBUG = False

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

    TODO
    - Come up with a more responsive way to do this - flexbox?
        Appears to be some inherent limitations in Streamlit
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
    
def changeMaxN():
    """
    Called when the selectbox in the welcome page is changed. The select box will have set 
    the st.session_state['maxN'] variable = what 2**maxN-1 should be..reverse that
    """

    if DEBUG:
        st.write(f"changeMaxN --- before maxN: {st.session_state['maxN']} type {type(st.session_state['maxN'])}")
        st.write(f"changeMaxN --- before upperLimit: {st.session_state['upperLimit']} type {type(st.session_state['upperLimit'])}")
    
    #-- User has selected a new upper limit. Update maxN accordingly
    if st.session_state['upperLimit'] != 2**st.session_state['maxN']-1 and st.session_state['upperLimit'] != 0:
        st.session_state['maxN'] = st.session_state['upperLimit'].bit_length()

    #-- the user's used the about page and upper limit is screwed
    #   Shift back to match maxN
    if st.session_state['upperLimit'] == 0:
        st.session_state['upperLimit'] = 2**st.session_state['maxN']-1


#-------------------
# Define the game stage pages
# - welcome
# - isYourNumberHere
# - isThisYourNumber

def welcome():
    """
    Display a welcome message
    """
    st.title("Can I read your mind??!!! Let's see...")

    st.markdown(f"""
1. Pick a number

    Pick any number between :red[1] and :red[{2**st.session_state['maxN']-1}] - :shushing_face::shushing_face: but don't tell me!!!

    (:information_source: Change the upper limit below)
2. Answer _Is your number below?_ {(2**st.session_state['maxN']-1).bit_length()} times.

    Each time you'll be shown a different list of numbers.
3. :tada::tada: I will tell you your number
""")

    st.button("Start!!", on_click=nextStage)

    #-- set index to the index of the current 2**maxN-1 value
    theOptions = [ 15, 31, 63, 127]
    if DEBUG:
        st.write(f"maxN: {st.session_state['maxN']} becomes {2**st.session_state['maxN']-1}")

    if DEBUG:
        st.write(f" 63 index: {theOptions.index(63)}")
        st.write(f"type maxN {type(st.session_state['maxN'])} ")

    optionIndex = theOptions.index( 2**st.session_state['maxN']-1 )


    if DEBUG:
        st.write(f"for maxN == {st.session_state['maxN']} becoming {2**st.session_state['maxN']-1} is found at index optionIndex: {optionIndex} i.e. {theOptions[optionIndex]}")

    st.subheader("Change the upper limit on the range")

    #-- kludge to make the selectbox not spread across the whole page
    col1, col2 = st.columns(2)
    col1.selectbox(
        "Choose from 1 to...", options=(15, 31, 63, 127), 
        index=optionIndex, key="upperLimit", label_visibility="visible"
        )

def nextStage():
    """
    Called when the user answers NO to _isYourNumberHere_ 

    Moves onto the next game stage and clears the page
    """

    if DEBUG:
        st.write(f"nextStage --- before gameStage: {st.session_state['gameStage']} type {type(st.session_state['gameStage'])}")
        st.write(f"nextStage --- before myGuess: {st.session_state['myGuess']} type {type(st.session_state['myGuess'])}")
        st.write(f"maxN: {st.session_state['maxN']} type {type(st.session_state['maxN'])}")

    st.session_state['gameStage'] += 1

    placeholder.empty()
    
def nextStageAddition():
    """
    Called when the user answers YES to _isYourNumberHere_

    Updates myGuess with the appropriate number and moves onto the next game stage
    """

    if DEBUG:
        st.write(f"nextStageAddition --- before gameStage: {st.session_state['gameStage']} type {type(st.session_state['gameStage'])}")
        st.write(f"nextStageAddition --- before myGuess: {st.session_state['myGuess']} type {type(st.session_state['myGuess'])}")
        st.write(f"maxN: {st.session_state['maxN']} type {type(st.session_state['maxN'])}")

    st.session_state['myGuess'] += 2**(st.session_state['gameStage'] - 1)
    st.session_state['gameStage'] += 1
    placeholder.empty()

def isYourNumberHere():
    """
    Based on gameStage display a table/list of appropriate numbers and ask the user if they see their number.

    Call nextStageAddition if the user answers YES
    Call nextStage if the user answers NO
    """
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
    """
    On the last stage, the user wishes to start again

    Reset game stage
    """
    st.session_state['gameStage'] = 0

def isThisYourNumber():
    """ 
    Present the user with their number and ask if they want to play again
    """
    st.title(f":tada::tada: You picked {st.session_state['myGuess']}!!!")

    st.button("Start again", on_click=startAgain)

#----------------------------
# Main execution loop
#
# - curate the session state and associated variables
# - decide which of the game stage functions to call


#-- Set up session state 

for var in 'gameStage', 'myGuess', 'upperLimit':
    if var not in st.session_state:
        st.session_state[var] = 0

if 'maxN' not in st.session_state:
    st.session_state['maxN'] = 6
    st.session_state['upperLimit'] = 63

gameStageFunctions = [
    welcome, isYourNumberHere, isThisYourNumber
]

if DEBUG:
    st.write(f"starting the main loop with {st.session_state['gameStage']} and maxN {st.session_state['maxN']} upperLimit {st.session_state['upperLimit']}")

changeMaxN()

#-- Call the appropriate game stage function

if st.session_state['gameStage'] == 0:
    st.session_state['myGuess'] = 0
    welcome()
elif st.session_state['gameStage'] <= st.session_state['maxN']:
    if DEBUG:
        st.write("-------- insert your number here")
    isYourNumberHere()
elif st.session_state['gameStage'] > st.session_state['maxN']:
    if DEBUG:
        st.write("-------- insert is this your number")
    isThisYourNumber()





