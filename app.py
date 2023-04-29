# -- Add "src" folder to the system Paths --
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from puzzle import Puzzle
from agents import Agent
import time
import streamlit as st  


def streamlitButton(txt_col="rgb(255, 255, 255)", txth_col="rgb(0, 0, 0)", bg_col="rgb(204, 49, 49)", bgh_color="rgb(255, 255, 255)"):
    """Modify the intial style of the Streamlit Buttons
    Args:
        txt_col (str, optional): Text color . Defaults to "rgb(255, 255, 255)".
        txth_col (str, optional): Text color when hovering. Defaults to "rgb(0, 0, 0)".
        bg_col (str, optional): Background color. Defaults to "rgb(204, 49, 49)".
        bgh_color (str, optional): Backgrond color when hovering. Defaults to "rgb(255, 255, 255)".
    """
    st.markdown("""
        <style>
            div.stButton {text-align: center;}
            div.stButton > button:first-child {background-color:""" + bg_col + """;color:""" + txt_col + """;}
            div.stButton > button:first-child:hover {background-color:""" + bgh_color + """;color:""" + txth_col + """;}
        </style>
    """, unsafe_allow_html=True)
    

def main():
    config_page_title, config_layout = 'Puzzle Multi-Agents', "wide"
    st.set_page_config(page_title=config_page_title, layout=config_layout)  # Set Page Configuration
    st.markdown("""<style>#MainMenu {visibility: visible;}footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 
    streamlitButton()

    if 'CONFIG' not in st.session_state:
        st.session_state['CONFIG'] = False
    
    if not st.session_state['CONFIG']:    
        
        with st.form(key='config_form'):
            st.write('<h3 style="text-align:center">Puzzle Multi-Agents - Configuration</h3>', unsafe_allow_html=True)
            _, col1, _, col2, _ = st.columns([2, 3.75, 0.5, 3.75, 2])
            sizeGrid = col1.number_input('Size of the Grid [n x n]', min_value=3, max_value=20, value=5, step=1)
            fillingGrid = col2.slider('Agents Filling Percentage [%]', min_value=30, max_value=100, value=80, step=10)
            _, col1, _, col2, _ = st.columns([2, 3.75, 0.5, 3.75, 2])
            displayTime = col1.number_input('Frequency of Grid Display', min_value=0.5, max_value=60.0, value=1.0, step=0.1)
            maxTime = col2.number_input('Max Execution Time', min_value=5, max_value=600, value=15, step=5)
            st.write("")
            button = st.form_submit_button(label='Start Simulation')

        placeholder = st.empty()
   
        if button:
            st.session_state['CONFIG'] = True
            Puzzle.agents = []
            Puzzle.grid=[]

            p = Puzzle(sizeGrid, fillingGrid)
            for target, pos in zip(p.position, p.target):
                Agent(pos, target)
                
            for agent in Puzzle.agents:
                agent.start()
                
            max_time = maxTime # seconds
            init_time = time.time()
            done = False

            st.session_state['GRID'] = [Puzzle.streamlitShowGrid()]
            while not done:
                time.sleep(displayTime)    
                placeholder.empty()
                with placeholder.container():
                    streamlitGRID = Puzzle.streamlitShowGrid()
                    
                    _, col1, _, col2, _ = st.columns([2, 3.75, 0.5, 3.75, 2])
                    
                    col1.write("""<h2 style="text-align:center">INITIAL GRID</h2>""", unsafe_allow_html=True)
                    col2.write("""<h2 style="text-align:center">CURRENT GRID</h2>""", unsafe_allow_html=True)

                    st.session_state['GRID'].append(streamlitGRID)
                    col1.write(st.session_state['GRID'][0], unsafe_allow_html=True)
                    col2.write(st.session_state['GRID'][-1], unsafe_allow_html=True)
                Puzzle.showGrid()

                
                complete = True
                for agent in Puzzle.agents:
                    if agent.current_position != agent.target_position:
                        complete = False
                        break
                if time.time() - init_time > max_time or complete:
                    done = True
                    print("FINAL GRID")
                    Puzzle.showGrid()
                    
                    
            for agent in Puzzle.agents:
                agent.running = False
            st.experimental_rerun()

    
    if st.session_state['CONFIG']:
        st.write('<h2 style="text-align:center">Puzzle Multi-Agents - Visualize the Grids</h2>', unsafe_allow_html=True)
        st.write('')
        _, col1, _ = st.columns([4, 4, 4])
        slide = col1.slider('Select the Grid', min_value=1, max_value=len(st.session_state['GRID']), value=1, step=1)
        st.write(f"""<h1 style="text-align:center">Grid {slide}</h1>""", unsafe_allow_html=True)
        st.write(st.session_state['GRID'][slide-1], unsafe_allow_html=True)
        st.write('')

        if st.button('New Configuration'):
            st.session_state['CONFIG'] = False
            st.experimental_rerun()


if __name__ == "__main__":
    main()