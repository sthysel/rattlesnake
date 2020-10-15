import click
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
#   volume:     The current volume.
#   segment:    The thread for the segment.
#   gradient:   The gradient of frequency / distance
#   intercept:  The value of frequency at distance = 0

class ToneManager:

    # Prepares a basic tone as default with volume and frequency
    def __init__ ( self, volume : float = 9, gradient : float = 200, intercept : float = 500 ):
        self.volume = volume
        self.gradient = gradient
        self.intercept = intercept

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
            # 100 seconds (arbitary number)
            # volume is in db from 0 being max.
            segment = self.tone.to_audio_segment(duration=10000, volume=((self.volume-9) * 5))
            playback.play(segment)



    # Maps the tone to a linear value.
    # x: The current value.
    # c: The value at x = 0.
    # m: The gradient.
    def map_tone ( self, x : float ):
        frequency = x * self.gradient + self.intercept
        self.play_tone(frequency)


    # Playes the specified frequency
    def play_tone ( self, freq : float ):
        print("Playing at: ", freq, "Hz")
        self.tone = generators.Sine(freq)
        self.reload()



    def set_volume ( self, vol : float ):
        self.volume = vol
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




@click.command()
@click.option('--min-distance',  default=0,    type=float,  help='The minimum expected distance from the sensor (highest tone).')
@click.option('--max-distance',  default=10,   type=float,  help='The maximum expected distance from the sensor (lowest tone).')
@click.option('--min-frequency', default=500,  type=float,  help='The minimum frequency expected to play (maximum distance).')
@click.option('--max-frequency', default=2500, type=float,  help='The maximum frequency expected to play (minimum distance).')
def start(min_distance:float, max_distance:float, min_frequency:float, max_frequency:float):

    '''
    This script will play a different tone depending on the proximity to the sensor.
    It uses a linear system where it will increase / decrease the tone depending on the distance.

    To change the performance during runtime, type:
        - on : Plays the tone
        - off: Stops the tone
        - f# : The frequency
        - d# : The distance from the sensor
        - v# : The volume (0 - 9)

        - 0  : exit (or ^c)
    '''

    gradient = (max_frequency - min_frequency) / (max_distance - min_distance)
    intercept = gradient * min_distance + min_frequency
    
    manager = ToneManager(gradient = gradient, intercept = intercept)
    usr = 'off'
    while ( input != 0 ):
        usr = click.prompt("enter something: ");
        if ( usr == 'on' ):
            manager.play()

        elif ( usr == 'off' ):
            manager.pause()
    
        elif (usr[0] == 'd'): # Distance
            manager.map_tone(float(usr[1:len(usr)]))

        elif (usr[0] == 'f'): # Frequency
            manager.play_tone(float(usr[1:len(usr)]))

        elif (usr[0] == 'v'): # Volume
            volume = int(usr[1:len(usr)])
            if ( volume < 10 ):
                manager.set_volume(volume)
                manager.reload()
            else:
                click.echo('enter a value < 9')

if __name__ == "__main__":
    start()












