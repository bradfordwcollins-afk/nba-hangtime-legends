echo off
del *.obj
del *.out
\tools\vidram on
del asm.log
echo NDSP1 >> asm.log
\tools\gspa NDSP1.axx NDSP1.obj -h -l -v10 >> asm.log
echo MAIN >> asm.log
\tools\gspa MAIN.axx MAIN.obj -h -l -v10 >> asm.log
echo UTIL >> asm.log
\tools\gspa UTIL.axx UTIL.obj -h -l -v10 >> asm.log
echo PAL >> asm.log
\tools\gspa PAL.axx PAL.obj -h -l -v10 >> asm.log
echo MPROC >> asm.log
\tools\gspa MPROC.axx MPROC.obj -h -l -v10 >> asm.log
echo BAKGND >> asm.log
\tools\gspa BAKGND.axx BAKGND.obj -h -l -v10 >> asm.log
echo BGNDTBL >> asm.log
\tools\gspa BGNDTBL.axx BGNDTBL.obj -h -l -v10 >> asm.log
echo BGNDPAL >> asm.log
\tools\gspa BGNDPAL.axx BGNDPAL.obj -h -l -v10 >> asm.log
echo IMGTBL >> asm.log
\tools\gspa IMGTBL.axx IMGTBL.obj -h -l -v10 >> asm.log
echo IMGPAL >> asm.log
\tools\gspa IMGPAL.axx IMGPAL.obj -h -l -v10 >> asm.log
echo BB >> asm.log
\tools\gspa BB.axx BB.obj -h -l -v10 >> asm.log
echo BB3 >> asm.log
\tools\gspa BB3.axx BB3.obj -h -l -v10 >> asm.log
echo PLYR >> asm.log
\tools\gspa PLYR.axx PLYR.obj -h -l -v10 >> asm.log
