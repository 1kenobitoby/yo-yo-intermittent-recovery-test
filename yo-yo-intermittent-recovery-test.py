import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Yo-Yo Intermittent Recovery Test App",
    page_icon="media/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    #menu_items={
        #'Get Help': '<<URL>>',
        #'Report a bug': "<<URL>>",
        #'About': "Made with Streamlit v1.27"
    #}
)

# html strings used to render donate button and link and text
donate_text = '<h6> Useful? Buy us a coffee. </h6>'

html_donate_button = '''
<form action="https://www.paypal.com/donate" method="post" target="_blank">
<input type="hidden" name="hosted_button_id" value="6X8E9CL75SRC2" />
<input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button"/>
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
</form>
'''   

def redirect_button(url: str):
    st.markdown(
    f"""
    <a href="{url}" target="_blank">
        <div>
        <img src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" alt="Donate with PayPal button">
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

st.image('media/logo.svg', width=100)
st.title('Yo-Yo Intermittent Recovery Test App')
   

st.write('This app shows you how to perform a Yo-Yo intermittent recovery level 1 test, [plays the audio](#audio_player) needed for the test and allows you to [enter the test score and interpret the result](#result). The Yo-Yo intermittent recovery level 1 test objectively measures a subject\'s fitness to perform repeated bouts of intense running. The Yo-Yo intermittent recovery tests are an alternative means of measuring running sport \'fitness\' to the more common continuous [beep shuttle running test](https://beep-test.streamlit.app/). In the Yo-Yo intermittent tests, the subject gets a short walk recovery after each pair of shuttle runs. As such, the Yo-Yo intermittent tests are felt to be a more specific and relevant test of the aerobic capacity of an individual performing sports which involve short bursts of intense activity with intervening rest periods (e.g. team sports like association football, rugby, cricket *etc.*). There are several different versions of the Yo-Yo tests: this app conducts what is known as the Yo-Yo intermittent recovery test level 1 which is by far the most commonly used version, used to test the aerobic fitness of non-elite level athletes. For a fuller explanation, expand the Notes section at the bottom of the page.')

tab_text, tab_video = st.tabs(["Text", "Video"])
with tab_text:
    st.subheader('How to set up and perform the test')
    st.write('1.    Find a level surface at least 25m long with good underfoot grip either indoors or on a windless day.')
    st.write('2.    Accurately measure out two lines 5m apart and a third line 20m beyond one of the other two. Mark out the lines so that test participants can see them while they are running between them. You can draw on the floor, use tape for the lines or mark the lines out with cones.')
    st.write('3.    Subjects start behind the line in the middle, facing the line 20m away. Start the audio player. The audio gives a 5 second warning then a double ascending beep tone starts the test. At the start of each run the audio will read out a speed level and run number (e.g. *"Five, one"* at the beginning of the test). Subjects should keep a mental note of what speed level and run number they are on as indicated by the audio announcement. The subjects run to the line 20m away. They must reach the other line by the time the audio next beeps (7.2 seconds after the start on the first speed level *five, one*). Subjects only have to \'toe the line\' i.e. touching the line with a foot is good enough, there is no requirement for them to completely cross it. If the subject reaches the other line before the next beep they must wait at the line until the next beep. At the beep subjects run back to the starting line.')
    st.write('4.    Subjects must reach the starting line before the next beep. Once that beep sounds, subjects have ten seconds to walk or jog to the line 5m away and back to the start line. After the 10 seconds has elapsed, a beep and announcement about speed level and run number will signal the start of the next pair of 20m shuttle runs.')
    st.write('5.    Periodically, after a recovery walk the audio will announce a change of running speed with *"Change to speed level ..."* and the double ascending beep tone will signal the start of the next 20m shuttle run. At each change of speed level the subjects have slightly less time to complete the 20m shuttle runs (although they still get 10 seconds to complete the recovery walk). Eventually a point will be reached where a subject has difficulty reaching the line before the next beep. When the subject fails to make the line before the next beep twice in a row the test ends. The subject notes the speed level and run number they were on when the test ended as announced by the audio player.')

with tab_video:
    st.video("https://www.elephant-stone.com/downloads/yo-yo-test-video.mp4", format='video/mp4')    


st.divider()
st.subheader('Test audio player', anchor='audio_player')
audio_file = open('media/yo_yo_intermittent_recovery_test_l1.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

st.divider()
st.subheader('Interpreting your test score', anchor='result')
level_col, shuttle_col = st.columns([1, 1])
with level_col:
    speed_level = st.number_input('What speed level did you reach?', min_value=5, max_value=23, step=1, value=None, help='For example, if the audio said "Fifteen, two" at the start of the run you were on when you were eliminated, you would enter 15 here')

with shuttle_col:
    shuttle = st.number_input('...and what run number were you on?', min_value=1, max_value=8, step=1, value=None, help='For example, if the audio said "Fifteen, two" at the start of the run you were on when you were eliminated, you would enter 2 here') 

st.write('\n')
if speed_level and shuttle:
    # Concatenate the level and shuttle into a string called lookup in the format '(L)LS'
    speed_level = str(speed_level)    
    shuttle = str(shuttle)   
    lookup = speed_level + shuttle
    # Cast 'lookup' back into an integer so you can use it as a lookup value in numerical pandas dataframe
    lookup=int(lookup)
    lookup_table = pd.read_csv('table.csv')
    # Check whether variable 'lookup' is in the 'level' column of the dataframe and either continue or send them back to reenter the level and shuttle.
    check_level = lookup in lookup_table['level'].values
    if check_level:
        # 'lookup' must be present in column 1 so find it in 'level' column and return item value from speed_kph column as mas variable
        speed = lookup_table.loc[lookup_table['level'] == lookup, 'Running_speed_kph'].item()
        speed_string = '<strong><em>The speed you were running at when the test ended was <span style="color:#F63366;"> ' + "%.1f" % speed + ' km h\u207B\u00B9</span></em></strong>'
        st.markdown(speed_string,  unsafe_allow_html=True)
        # Wash, rinse repeat for distance covered, time taken and VO2max
        dist = lookup_table.loc[lookup_table['level'] == lookup, 'Cum_distance_m'].item()
        time = lookup_table.loc[lookup_table['level'] == lookup, 'Cum_time_inc_recov_secs'].item()
        run_string = '<strong><em>You ran a total distance of <span style="color:#F63366;"> ' + "%.0f" % dist + ' metres</span> in <span style="color:#F63366;">' + "%.0f" % time + ' seconds</span></em></strong>'
        st.markdown('\n')
        st.markdown(run_string,  unsafe_allow_html=True)
        st.markdown('\n')
        st.markdown('<strong><em>Here\'s how your distance compares to [published studies](https://elephant-stone.com/downloads/yo-yo-test-refs/Schmitz_et_al_2018.pdf) of groups of competitors from a range of different sports and fitness levels.</em></strong>', unsafe_allow_html=True)
        st.image('media/Figure_1.png', use_column_width=True, caption='Figure 1. Test results for a range of sports and player standards. To see how you compare, find your distance on the axis of the right hand chart and read up vertically until you reach the group you wish to compare yourself with. Each horizontal line shows how a group performed. 20% of subjects scored lower than the left hand circle; 20% of subjects scored higher than the right hand circle. The other 60% were spread along the line. Abbreviations: RS, rugby sevens; GF, gaelic football.')
        with st.expander('Why no VO\u2082max?'):
            st.write('VO\u2082max is a person\'s maximal rate of oxygen consumption. It is a useful thing to know because it fairly accurately predicts the person\'s potential finishing time over various distance running races. Attempts have been made to correlate Yo-Yo intermittent recovery test results with VO\u2082max but the data are horribly scattered so the calculated values have a large error bar (see Figure 12 of [Bangsbo et al, 2008](https://elephant-stone.com/downloads/yo-yo-test-refs/Bangsbo_et_al_2008.pdf)). VO\u2082max is a measure of aerobic capacity. In the intermittent recovery tests, the subject is going anaerobic during the shuttle runs with the aerobic system repaying the oxygen debt during the recovery phase. Consequently the intermittent recovery tests aren\'t measuring aerobic capacity, more the ability to do intense periods of partly anaerobic work and recover rapidly using the aerobic system. If you want to know your VO\u2082max and use it to calculate distance running race potential you\'ll get a much more reliable value by doing a continuous running beep test [using this app](https://beep-test.streamlit.app).')

    else:
        st.markdown('<strong><em>You seem to have entered an impossible combination of level and shuttle number. Check your inputs.</em></strong>', unsafe_allow_html=True)     
    

st.divider()





st.write('\n')
st.write('\n')
donate_left, donate_right = st.columns([1, 3])
with donate_left:
    st.write('\n')
    st.markdown(donate_text, unsafe_allow_html=True)

with donate_right:
    st.write('\n')
    redirect_button("https://www.paypal.com/donate/?hosted_button_id=6X8E9CL75SRC2")   

st.write('\n')
st.write('\n')
notes = st.button('Notes:small_red_triangle_down:')

notes_container1 = st.empty()
if notes:
    notes_string = 'The Yo-Yo intermittent recovery tests were developed by a Danish physiologist and former national soccer player called Jens Bangsbo in the early 1990s. Tests of \'fitness\' for running sports using continuous running tests had become popular by this time. However some questioned the relevance of being able to run continuously for many team sports that involved short bursts of intense sprinting, jumping or turning and pushing off followed by rest periods. Bangsbo developed the Yo-Yo intermittent recovery tests as a development of the [continuous beep test](https://beep-test.streamlit.app). The test methods were originally [published in a book](https://www.waterstones.com/book/fitness-training-in-football/jens-bangsbo/9788798335078) which is now out of print. A description of the tests and demonstrations of their worth and validity can be found in [Bangsbo et al, 2008](https://elephant-stone.com/downloads/yo-yo-test-refs/Bangsbo_et_al_2008.pdf). <br>Confusingly, there are now six different Yo-Yo tests. Test scores and levels are not comparable between them so if someone says they have done a Yo-Yo test, make sure you are talking about the same thing. The different tests are:<ul><li>Yo-Yo Endurance Test Level 1. This is exactly the same as a [beep test](https://beep-test.stremalit.app)</li><li>Yo-Yo Endurance Test Level 2. A continuous running beep test but starting at a faster speed than a regular beep test</li><li>Yo-Yo Intermittent Endurance Test Level 1. This is similar to the test in this app but you only get a 5 second break at the end of each pair of 20m shuttle runs</li><li>Yo-Yo Intermittent Endurance Test Level 2. The same as the level 1 test above but starting at a higher running speed</li><li>Yo-Yo Intermittent Recovery Test Level 1. ***The test that is used in this app***. The most popular version of the Yo-Yo tests with two 20m shuttle runs starting at 10km h\u207B\u00B9 and getting progressively faster followed by a 10 second walk recovery</li><li>Yo-Yo Intermittent Recovery Test Level 2. The same procedure as the Level 1 Intermittent Recovery Test but starting at a faster running speed so intended for elite level sportspeople</li></ul><br>The procedure for the intermittent recovery test level 1 (which this app uses) is three runs at between 10 and 13km h\u207B\u00B9, with running speeds increasing by 0.5km h\u207B\u00B9 for each level after that. All versions of the test use 10 and 13km h\u207B\u00B9 for two of the first three runs. The speed of the other one wasn\'t originally specified though so some tests use 11.5km h\u207B\u00B9 while others (including the one in this app) use 12km h\u207B\u00B9. It makes little  practical difference: hardly anyone goes out on the second speed level and the difference in time spent running is half a second. In case you are interested, the speed levels that the audio talks about are directly related to the running speed:<br>&emsp;*Speed level = 2 x [(Running speed in km h\u207B\u00B9) - 7.5]*<br>As the running speed gets progressively faster, eventually a point will be reached where the participant can\'t keep up with the beeps. When the participant fails twice in a row to make it to the next line before the beep sounds the test ends. The participant notes the level and run number they were on when they were eliminated. This forms the input to the app which tells you your performance. <br>In this app we don\'t use what are known as normative tables. These are lookup tables which tell the participant based on their score whether they are \'good\', or \'average\' or \'very poor\'. It\'s self-evident that if you reach speed level 15, 2 you have done better than if you had reached 14, 2. There are so many different sets of published normative tables that comparisons are at best confusing and at worst meaningless. The tables are comparing your performance to that of a test group published in academic literature. But without knowing who your comparision group is this means little. Figure 1 which appears with your results shows how you compare with published studies from a wide range of sports and performance levels. Internet searching will also reveal many test results from professional players in various sports although the reliability of these claims is often unclear.<br>If you want to improve your score, many people will find that they improve somewhat just by repeating the test a few times to gain familiarity with the pacing and technique. Some tips here are: don\'t run any faster than you have to (arrive at the line in time with the next beep rather than getting there early and having to wait); you only have to touch the line with your toe so don\'t run too far by going over the line; Once you\'ve got the technique down though, to improve you\'ll have to get fitter. The Yo-Yo test is mentally and physically tough because it\'s a maximal effort so don\'t do it more than once or twice a week. If you need to improve, interval and repetition training are the way to go. Interval training where you do repeated runs at about the pace you could maintain for 20 minutes in intervals of about 3 to 5 minutes with similar length rest periods develop your aerobic capacity to recover during the walk phase. Repeated repetition runs of up to 2 minutes at about the pace you could maintain for about a mile with full recoveries in between build your speed. If you have a heart rate monitor you can use [this app](https://hr-training-zones-calculator.streamlit.app) to help you get the training right.<br><small>*Comments, queries or suggestions? [Contact us](https://www.elephant-stone.com/contact.html)*.</small>'
    notes_container1.markdown(notes_string, unsafe_allow_html=True)
    hide =st.button('Hide notes:small_red_triangle:')
    if hide:
        notes = not notes
        notes_container1 = st.empty()    

