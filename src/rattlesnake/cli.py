import pydub
from pydub import generators
from pydub import playback
import multiprocessing



# Plays specified tone.
# Uses pydub to generate tone.
# pydub could be used to play audio files as well by changing segment to your choice of audio segments from pydub.
# The type of wave can also be changed (currently Sine).
#
#
# Object variables:
# volume
# segment

class ToneManager:

    # Prepares a basic tone as default with volume and frequency
    def __init__ ( self, volume:float = 0.5 ):
        self.volume = volume
        self.thread = multiprocessing.Process(target=self._sound_thread_player)

        self.play_tone(0)
        self.pause()

    # Destructor
    def __del__ ( self ):
        self.pause()


    # THIS IS A THREAD
    # Loops the specific frequency and updates at the end of each wave.
    def _sound_thread_player ( self ):
        while ( True ):
            playback.play(self.segment)



    # Maps the tone to a linear value.
    # x: The current value.
    # c: The value at x = 0.
    # m: The gradient.
    def map_tone ( self, x : float, m : float = 200.0, c : float = 500.0 ):
        frequency = x * m + c
        self.play_tone(frequency)


    # Playes the specified frequency
    def play_tone ( self, freq : float  ):
        print("Playing at: ", freq, "Hz")
        tone = generators.Sine(freq)
        self.segment = tone.to_audio_segment(duration=10000) # 100 seconds (arbitary number)
        self.reload()



    # Begins the tone.
    def play ( self ):
        if ( self.thread.is_alive() ):
            self.pause()
        self.thread = multiprocessing.Process(target=self._sound_thread_player)
        self.thread.start()

    # Ends the tone.
    def pause ( self ):
        if ( self.thread.is_alive() ):
            self.thread.terminate()

    # Calls pause then play to reload the tone
    def reload ( self ):
        self.pause()
        self.play()




# User Input, Front End Code
manager = ToneManager()
usr = 'off'
while ( input != 0 ):
    usr = input("enter something: ");


    if ( usr == 'on' ):
        manager.play()
    elif ( usr == 'off' ):
        manager.pause()
    
    else:
        manager.map_tone(float(usr))
