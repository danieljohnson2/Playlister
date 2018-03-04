# Playlister
Creates playlists for a 2018 Subaru Legacy head unit.

When Old Scratch designed the audio for the 2018 Subaru Legacy,
Subaru took one look and told him "Satan, go home. You're drunk."
But then they shipped it anyway!

Okay, maybe it isn't *that* bad, but it sure makes a terrible first
impression.

The worst part is that it turns on the radio whenever you start or stop the car.
The best advice I can give you is to tune it to to XM Radio channel 0; there's
no audio on that channel at least.

You can then still play audio off a USB stick. But it doesn't know what folders
are. It can only find audio files by metadata, and it plays them in alphabetical
order (by the track name in the metadata, not file name).

Then there's a disabled "Playlist" button intead, but no way to make one. This
little script makes playlists that work.

What the Subie is looking for are playlist files that share the name of the
directory they appear in, but with an ".m3u" extension, and which must contain
newline-separated relative paths to the individual files. Each path must end in
an ".mp3" or ".wma" file extension.

The media files can be in subdirectories, and the playlist file controls the
order of playback.

To use playlister, run it on the command line and pass a directory or
directories to make playlists for:

```bash
./playlister.py ~/Music/*
./playlister.py ~/Music/Banjo ~/Music/Kazoo
```

This will create ~/Music/Banjo/Banjo.m3u and ~/Music/Kazoo/Kazoo.m3u. It
won't create a separate playlist for ~/Music/Kazoo/Orchestral, but will
include those tracks in Kazoo.m3u.

I've tested this only on Linux, but I think it should work on Windows or
Mac OS X if you have Python there.
