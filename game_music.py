import pygame

class MusicPlayer(object):
    music_path = "./res/sound/"
    def __init__(self,bgmusic,wav_names):
        pygame.mixer.music.load(self.music_path + bgmusic)
        pygame.mixer.music.set_volume(0.1)
        self.pms={}
        for wav in wav_names:
            self.pms[wav]=pygame.mixer.Sound(self.music_path+wav)

        print(self.pms)

    def play_bg(self):
        pygame.mixer.music.play(-1)

    def pause_bg(is_pause):
        if is_pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def play_sound(self,wav_name):
        self.pms[wav_name].set_volume(0.5)
        self.pms[wav_name].play()
