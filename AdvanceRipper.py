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
romLoc+=4
tableOffset=rom[romLoc]+(rom[romLoc+1]*0x100)+(rom[romLoc+2]*0x10000)+((rom[romLoc+3]&0x7)*0x1000000)
romLoc+=4
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
pointerFix = []
pointerFix.append(8) #address 0x8 table pointer
pointerFix.append(len(out)) #pointer where table will be put

keyPointer = []
kSplitPointer = []
aSplitPointer = []
instPointer = []
wavPointer = []
romLoc=tableOffset
for i in range(128):
	type=rom[romLoc]
	out.append(rom[romLoc])
	out.append(rom[romLoc+1])
	out.append(rom[romLoc+2])
	out.append(rom[romLoc+3])
	if(type==0x00 or type==0x08):
		instPointer.append(len(out))
		instPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))
	elif(type==0x03 or type==0x0B):
		wavPointer.append(len(out))
		wavPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))
	elif(type==0x40):
		kSplitPointer.append(len(out))
		kSplitPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))
		keyPointer.append(len(out)+4)
		keyPointer.append(rom[romLoc+8]+(rom[romLoc+9]*0x100)+(rom[romLoc+10]*0x10000)+((rom[romLoc+11]&0x7)*0x1000000))
	elif(type==0x80):
		aSplitPointer.append(len(out))
		aSplitPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))

	out.append(rom[romLoc+4])
	out.append(rom[romLoc+5])
	out.append(rom[romLoc+6])
	out.append(rom[romLoc+7])
	out.append(rom[romLoc+8])
	out.append(rom[romLoc+9])
	out.append(rom[romLoc+10])
	out.append(rom[romLoc+11])
	romLoc+=12

for i in range(len(keyPointer)>>1):
	romLoc=keyPointer[(i*2)+1]
	pointerFix.append(keyPointer[(i*2)])
	pointerFix.append(len(out))
	max = 0
	for ii in range(128):
		out.append(rom[romLoc])
		if(rom[romLoc]>max):
			max=rom[romLoc]
		romLoc+=1
	romLoc=kSplitPointer[(i*2)+1]
	pointerFix.append(kSplitPointer[(i*2)])
	pointerFix.append(len(out))
	for ii in range(max):
		type=rom[romLoc]
		out.append(rom[romLoc])
		out.append(rom[romLoc+1])
		out.append(rom[romLoc+2])
		out.append(rom[romLoc+3])
		if(type==0x00 or type==0x08):
			instPointer.append(len(out))
			instPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))
		elif(type==0x03 or type==0x0B):
			wavPointer.append(len(out))
			wavPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))

		out.append(rom[romLoc+4])
		out.append(rom[romLoc+5])
		out.append(rom[romLoc+6])
		out.append(rom[romLoc+7])
		out.append(rom[romLoc+8])
		out.append(rom[romLoc+9])
		out.append(rom[romLoc+10])
		out.append(rom[romLoc+11])
		romLoc+=12

for i in range(len(aSplitPointer)>>1):
	romLoc=aSplitPointer[(i*2)+1]
	pointerFix.append(aSplitPointer[(i*2)])
	pointerFix.append(len(out))
	for ii in range(128):
		type=rom[romLoc]
		out.append(rom[romLoc])
		out.append(rom[romLoc+1])
		out.append(rom[romLoc+2])
		out.append(rom[romLoc+3])
		if(type==0x00 or type==0x08):
			instPointer.append(len(out))
			instPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))
		elif(type==0x03 or type==0x0B):
			wavPointer.append(len(out))
			wavPointer.append(rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000))

		out.append(rom[romLoc+4])
		out.append(rom[romLoc+5])
		out.append(rom[romLoc+6])
		out.append(rom[romLoc+7])
		out.append(rom[romLoc+8])
		out.append(rom[romLoc+9])
		out.append(rom[romLoc+10])
		out.append(rom[romLoc+11])
		romLoc+=12

for i in range(len(wavPointer)>>1):
	romLoc=wavPointer[(i*2)+1]
	pointerFix.append(wavPointer[(i*2)])
	pointerFix.append(len(out))
	for ii in range(16):
		out.append(rom[romLoc])
		romLoc+=1

for i in range(len(instPointer)>>1):
	romLoc=instPointer[(i*2)+1]
	pointerFix.append(instPointer[(i*2)])
	pointerFix.append(len(out))
	instSize=rom[romLoc+12]+(rom[romLoc+13]*0x100)+(rom[romLoc+14]*0x10000)+((rom[romLoc+15]&0x7)*0x1000000)
	instSize+=19 #add in the header plus 3 extra sample bytes
	for ii in range(instSize):
		out.append(rom[romLoc])
		romLoc+=1
		
for i in range(len(pointerFix)>>1):
	romLoc=pointerFix[(i*2)]
	out[romLoc]=((pointerFix[(i*2)+1])&0xFF)
	out[romLoc+1]=(((pointerFix[(i*2)+1])&0xFF00)>>8)
	out[romLoc+2]=(((pointerFix[(i*2)+1])&0xFF0000)>>16)
	out[romLoc+3]=(((pointerFix[(i*2)+1])&0xFF000000)>>24)
	
outfile=open(sysargv[1].replace(".gba",".bin"),"wb")
for i in range(len(out)):
	outfile.write(out[i].to_bytes(1,byteorder='little'))
outfile.close()
