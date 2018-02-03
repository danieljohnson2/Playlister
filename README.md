# Playlister
Creates playlists for a 2018 Subaru Legacy head unit.

When Old Scratch designed the audio for the 2018 Subaru Legacy,
Subaru took one look and told him "Satan, go home. You're drunk."
But then they shipped it anyway!

You can play audio off a USB stick, but the thing doesn't know what folders are.
It can only find audio files by metadata, and it plays them in alphabetical order
(by the track name in the metadata, not file name).

There's a disabled "Playlist" button intead, but no way to make one. This little script makes
playlists that work.

As I understand it, what the Subie is looking for are playlist files that share the name of
the directory they appear in, but with an ".m3u" extension, and which must contain newline-separated
relative paths to the individual files. They can be in subdirectories, and the playlist file
controls the order of playback.

If you are looking to stop the thing from turning on the radio when you start or stop the car,
I haven't found a way to do that. It seems like tuning to XM Radio channel 0 helps; there's no
audio on that channel at least.

To use playlister, run it on the command line and pass a directory or directories to make playlists for:

```bash
./playlister.py ~/Music/*
./playlister.py ~/Music/Banjo ~/Music/Kazoo
```

I've tested this only on Linux, but I think it should work on Windows or Mac OS X if you have Python there.
