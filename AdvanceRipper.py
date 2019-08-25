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
	
romSize=len(rom)
out = []
songOffset = []
tableOffset = []
pointerFix = []
numSongs = 0
tempOffset = offset
searching = True
while(searching):
	if(rom[tempOffset+3]==0x08): #probably a song pointer
		songOffset.append(rom[tempOffset]+(rom[tempOffset+1]*0x100)+(rom[tempOffset+2]*0x10000)+((rom[tempOffset+3]&0x7)*0x1000000))
		numSongs+=1
	else:
		searching = False
	tempOffset+=8
	
if(numSongs==0):
	sys.exit()

print("\nFound "+str(numSongs)+" songs\n")
tempOffset = offset
out.append(numSongs&0xFF)
out.append((numSongs&0xFF00)>>8)
out.append((numSongs&0xFF0000)>>16)
out.append((numSongs&0xFF000000)>>24)
for i in range(numSongs):
	out.append(rom[tempOffset])
	out.append(rom[tempOffset+1])
	out.append(rom[tempOffset+2])
	out.append(rom[tempOffset+3])
	out.append(rom[tempOffset+4])
	out.append(rom[tempOffset+5])
	out.append(rom[tempOffset+6])
	out.append(rom[tempOffset+7])
	tempOffset+=8
	
print("Writing:")
for si in range(numSongs):
	romLoc=songOffset[si]
	if(romLoc!=0xFFFFFFFF):			
		print(str(si)+" @ "+str(romLoc))
		pointerFix.append((si*8)+4) #address to be adjusted
		pointerFix.append(len(out)) #new pointer	
		for ti in range(numSongs): #check for duplicate pointers, so pointed data is written once, but all pointers are fixed
			if(ti<=si):
				ti=si+1
			if(ti<numSongs):
				if(songOffset[ti]==romLoc):
					pointerFix.append((ti*8)+4)
					pointerFix.append(len(out))
					songOffset[(ti)]=0xFFFFFFFF
		numChannels=rom[romLoc]+(rom[romLoc+1]*0x100)
		if(numChannels>0):
			romLoc+=4
			tableOffset.append(len(out)+8)
			tableOffset.append(rom[romLoc]+(rom[romLoc+1]*0x100)+(rom[romLoc+2]*0x10000)+((rom[romLoc+3]&0x7)*0x1000000))
			romLoc+=4
			ch1Offset=rom[romLoc]+(rom[romLoc+1]*0x100)+(rom[romLoc+2]*0x10000)+((rom[romLoc+3]&0x7)*0x1000000)
			romLoc=songOffset[si]
			pointerOffset=(ch1Offset+0x08000000)-(((numChannels+3)*4)+len(out))
			out.append(pointerOffset&0xFF)
			out.append((pointerOffset&0xFF00)>>8)
			out.append((pointerOffset&0xFF0000)>>16)
			out.append((pointerOffset&0xFF000000)>>24)
			for i in range((numChannels+2)*4):
				out.append(rom[romLoc])
				romLoc+=1
			songSize=songOffset[si]-ch1Offset
			romLoc=ch1Offset
			for i in range(songSize):
				out.append(rom[romLoc])
				romLoc+=1

keyPointer = []
kSplitPointer = []
aSplitPointer = []
instPointer = []
wavPointer = []

print("\nFound "+str(len(tableOffset)>>1)+" tables\nWriting:")
for si in range(len(tableOffset)>>1):
	romLoc=tableOffset[(si*2)+1]
	if(romLoc!=0xFFFFFFFF):
		print(str(si)+" @ "+str(romLoc))
		pointerFix.append(tableOffset[(si*2)])
		pointerFix.append(len(out))
		for ti in range(len(tableOffset)>>1):
			if(ti<=si):
				ti=si+1
			if(ti<(len(tableOffset)>>1)):
				if(tableOffset[(ti*2)+1]==romLoc):
					pointerFix.append(tableOffset[(ti*2)])
					pointerFix.append(len(out))
					tableOffset[(ti*2)]=0xFFFFFFFF
					tableOffset[(ti*2)+1]=0xFFFFFFFF
		for i in range(128):
			type=rom[romLoc]
			out.append(rom[romLoc])
			out.append(rom[romLoc+1])
			out.append(rom[romLoc+2])
			out.append(rom[romLoc+3])
			tempPointer=rom[romLoc+4]+(rom[romLoc+5]*0x100)+(rom[romLoc+6]*0x10000)+((rom[romLoc+7]&0x7)*0x1000000)
			tempPointer2=rom[romLoc+8]+(rom[romLoc+9]*0x100)+(rom[romLoc+10]*0x10000)+((rom[romLoc+11]&0x7)*0x1000000)
			if(rom[romLoc+7]==0x08):
				if(type==0x00 or type==0x08):
					instPointer.append(len(out))
					instPointer.append(tempPointer)
					if(tempPointer>=romSize):
						print("Out of bounds pointer @ "+str(romLoc+4))
						sys.exit()
				elif(type==0x03 or type==0x0B):
					wavPointer.append(len(out))
					wavPointer.append(tempPointer)
					if(tempPointer>=romSize):
						print("Out of bounds pointer @ "+str(romLoc+4))
						sys.exit()
				elif(type==0x40):
					if(rom[romLoc+11]==0x08):
						kSplitPointer.append(len(out))
						kSplitPointer.append(tempPointer)
						if(tempPointer>=romSize):
							print("Out of bounds pointer @ "+str(romLoc+4))
							sys.exit()
						keyPointer.append(len(out)+4)
						keyPointer.append(tempPointer2)
						if(tempPointer2>=romSize):
							print("Out of bounds pointer @ "+str(romLoc+8))
							sys.exit()
				elif(type==0x80):
					aSplitPointer.append(len(out))
					aSplitPointer.append(tempPointer)
					if(tempPointer>=romSize):
						print("Out of bounds pointer @ "+str(romLoc+4))
						sys.exit()

			out.append(rom[romLoc+4])
			out.append(rom[romLoc+5])
			out.append(rom[romLoc+6])
			out.append(rom[romLoc+7])
			out.append(rom[romLoc+8])
			out.append(rom[romLoc+9])
			out.append(rom[romLoc+10])
			out.append(rom[romLoc+11])
			romLoc+=12

print("\nFound "+str(len(keyPointer)>>1)+" key splits\nWriting:")
for i in range(len(keyPointer)>>1):
	romLoc=keyPointer[(i*2)+1]
	if(romLoc!=0xFFFFFFFF):
		print(str(i)+" @ "+str(romLoc))
		pointerFix.append(keyPointer[(i*2)])
		pointerFix.append(len(out))
		for ti in range(len(keyPointer)>>1):
			if(ti<=i):
				ti=i+1
			if(ti<(len(keyPointer)>>1)):
				if(keyPointer[(ti*2)+1]==romLoc):
					pointerFix.append(keyPointer[(ti*2)])
					pointerFix.append(len(out))
					keyPointer[(ti*2)]=0xFFFFFFFF
					keyPointer[(ti*2)+1]=0xFFFFFFFF
		max = 0
		for ii in range(128):
			out.append(rom[romLoc])
			if(rom[romLoc]>max):
				max=rom[romLoc]
			romLoc+=1
		romLoc=kSplitPointer[(i*2)+1]
		pointerFix.append(kSplitPointer[(i*2)])
		pointerFix.append(len(out))
		if(max>0x7F):
			max=0x7F
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

print("\nFound "+str(len(aSplitPointer)>>1)+" sub tables\nWriting:")
for i in range(len(aSplitPointer)>>1):
	romLoc=aSplitPointer[(i*2)+1]
	if(romLoc!=0xFFFFFFFF):
		print(str(i)+" @ "+str(romLoc))
		pointerFix.append(aSplitPointer[(i*2)])
		pointerFix.append(len(out))
		for ti in range(len(aSplitPointer)>>1):
			if(ti<=i):
				ti=i+1
			if(ti<(len(aSplitPointer)>>1)):
				if(aSplitPointer[(ti*2)+1]==romLoc):
					pointerFix.append(aSplitPointer[(ti*2)])
					pointerFix.append(len(out))
					aSplitPointer[(ti*2)]=0xFFFFFFFF
					aSplitPointer[(ti*2)+1]=0xFFFFFFFF
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

print("\nFound "+str(len(wavPointer)>>1)+" PSG Waves\nWriting:")
for i in range(len(wavPointer)>>1):
	romLoc=wavPointer[(i*2)+1]
	if(romLoc!=0xFFFFFFFF):
		print(str(i)+" @ "+str(romLoc))
		pointerFix.append(wavPointer[(i*2)])
		pointerFix.append(len(out))
		for ti in range(len(wavPointer)>>1):
			if(ti<=i):
				ti=i+1
			if(ti<(len(wavPointer)>>1)):
				if(wavPointer[(ti*2)+1]==romLoc):
					pointerFix.append(wavPointer[(ti*2)])
					pointerFix.append(len(out))
					wavPointer[(ti*2)]=0xFFFFFFFF
					wavPointer[(ti*2)+1]=0xFFFFFFFF
		for ii in range(16):
			out.append(rom[romLoc])
			romLoc+=1

print("\nFound "+str(len(instPointer)>>1)+" PCM Waves\nWriting:")
for i in range(len(instPointer)>>1):
	romLoc=instPointer[(i*2)+1]
	if(romLoc!=0xFFFFFFFF):
		print(str(i)+" @ "+str(romLoc))
		pointerFix.append(instPointer[(i*2)])
		pointerFix.append(len(out))
		for ti in range(len(instPointer)>>1):
			if(ti<=i):
				ti=i+1
			if(ti<(len(instPointer)>>1)):
				if(instPointer[(ti*2)+1]==romLoc):
					pointerFix.append(instPointer[(ti*2)])
					pointerFix.append(len(out))
					instPointer[(ti*2)]=0xFFFFFFFF
					instPointer[(ti*2)+1]=0xFFFFFFFF
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

print("\nWriting to file...")
outfile=open(sysargv[1].replace(".gba",".bin"),"wb")
for i in range(len(out)):
	outfile.write(out[i].to_bytes(1,byteorder='little'))
	
print("\nDone!")
outfile.close()
