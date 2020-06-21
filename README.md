# noisterous
Digital trumpet on the raspberry Pi using an Xbox controller


## Install libraries

`sudo apt-get install timidity`
`sudo apt-get install fluidsynth alsa-utils -y`
`sudo apt-get install fluid-soundfont-gm`

## Setup Raspberry Pi

`sudo nano /etc/timidity/timidity.cfg`
Add `source /etc/timidity/fluidr3_gm.cfg`

`sudo nano /etc/rc.local`
Add `timidity -iA`