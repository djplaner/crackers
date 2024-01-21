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


import streamlit as st

about = """
## Origins

Awareness of this "game" came from [this description](https://www.youcubed.org/tasks/crackers/) introduced by [Cathy Williams](https://www.linkedin.com/in/youcubedwilliams/). Crackers is intended as a [low floor, high ceiling](https://djplaner.github.io/memex/sense/Teaching/low-floor-high-ceiling-wide-walls/) mathematics learning task. The name is inspired by Cathy's memories of a prize from a Cracker Jack box. 

This version of the game was developed to:

1. Experiment with [Streamlit](https://streamlit.io) to create simple web applications.
2. Possibly use in a classroom introducing [binary data representation](https://djplaner.github.io/memex/sense/Teaching/Mathematics/crackers/#re-purposing-as-an-activity-for-teaching-digital-technologies)

## For more

- [Cracker's GitHub repository](https://github.com/djplaner/crackers) 
- [YouCubed's description of Crackers](https://www.youcubed.org/tasks/crackers/) including suggested questions to frame student engagement with the task.

"""

st.title('About "_Crackers_"')

st.markdown(about)
