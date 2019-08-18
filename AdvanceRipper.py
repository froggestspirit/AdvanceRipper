#sonic factory 963648
#AdvanceRipper by FroggestSpirit
version="0.1"
#Rip M4A engine soundtracks from GBA roms
#Make backups, this can overwrite files without confirmation
#Usaage: "AdvanceRipper.py" "input.gba" "address of song table"
import sys
import math

sysargv=sys.argv
echo=True
mode=0
print("GBARipper "+version+"\n")
infileArg=-1;
outfileArg=-1;
if(len(sysargv)==3):
	infile=open(sysargv[1], "rb")
	rom=infile.read()
	infile.close()
	offset=int(sysargv[2])
else:
	sys.exit()

out = []
#out.append(ord('M'))
songOffset=rom[offset]+(rom[offset+1]*0x100)+(rom[offset+2]*0x10000)+((rom[offset+3]&0x7)*0x1000000)
romLoc=songOffset
numChannels=rom[romLoc]+(rom[romLoc+1]*0x100)
romLoc+=8
ch1Offset=rom[romLoc]+(rom[romLoc+1]*0x100)+(rom[romLoc+2]*0x10000)+((rom[romLoc+3]&0x7)*0x1000000)
romLoc=songOffset
pointerOffset=ch1Offset-((numChannels+3)*4)
out.append(pointerOffset&0xFF)
out.append((pointerOffset&0xFF00)>>8)
out.append((pointerOffset&0xFF0000)>>16)
out.append((pointerOffset&0xFF000000)>>24)
for i in range((numChannels+2)*4):
	out.append(rom[romLoc])
	romLoc+=1
songSize=songOffset-ch1Offset
romLoc=ch1Offset
for i in range(songSize):
	out.append(rom[romLoc])
	romLoc+=1

outfile=open(sysargv[1].replace(".gba",".bin"),"wb")
for i in range(len(out)):
	outfile.write(out[i].to_bytes(1,byteorder='little'))
outfile.close()