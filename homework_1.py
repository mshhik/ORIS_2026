class Playlist():
    def __init__(self):
        self.songs = []
        
        
    def add_song(self, name: str, duration: int):
        song = {
            'name': name,
            'duration': duration
        }
        self.songs.append(song)
    
    
    def remove_song(self, name: str):
        for song in self.songs:
            if song['name'] == name:
                self.songs.remove(song)
                return
    
    def total_duration(self):
        total = 0
        
        for song in self.songs:
            total += song['duration']
        
        return total
    
    
    def __len__(self):
        return len(self.songs)
    
    
    def show_songs(self):
        if not self.songs:
            print('Плейлист пустой')
            return
        
        print('Список песен:')
        
        for number, song in enumerate(self.songs, start=1):
            print(f'{number}. {song['name']} - {song['duration']} сек.')
    
    
playlist = Playlist()
playlist.add_song('Billie Jean', 293)
playlist.add_song('Монополия', 217)
playlist.remove_song('Монополия')
#playlist.remove_song('Billie Jean')
playlist.remove_song('pack up your bags')
print(f'Общая продолжительность плейлиста: {playlist.total_duration()}')
print(f'Количество песен в плейлисте: {len(playlist)}')
playlist.show_songs()