AdvanceRipper

Rip M4A engine soundtracks from GBA roms into a "lightweight" bin file
Make backups, this can overwrite files without confirmation!

Usage: "AdvanceRipper.py" "input.gba" "address of song table"

This will output music data as a bin file, with the same name and path as the input file.

Format is:
0x00-0x03: number of songs
0x04: song table

The rest is the same format as from the GBA rom, with a few exceptions. Each song header now has a 4 byte offset at (0x00 + song pointer)
This offset is to be subtracted from any 4 byte pointer in the song's sequence data to get the correct absolute position (with the exception of the instrument table pointer, which is corrected).
Every other absolute pointer outside of song data is corrected to point to the absolute position in the file.

The program will try to identify data with the same pointer, so if a song or instrument has multiple pointers to the same data, it will only write the data once.
