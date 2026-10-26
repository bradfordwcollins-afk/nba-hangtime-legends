echo off
\tools\vidram on
echo SELECT >> asm.log
\tools\gspa SELECT.axx SELECT.obj -h -l -v10 >> asm.log
echo SELECT2 >> asm.log
\tools\gspa SELECT2.axx SELECT2.obj -h -l -v10 >> asm.log
echo STRING >> asm.log
\tools\gspa STRING.axx STRING.obj -h -l -v10 >> asm.log
echo RECORD >> asm.log
\tools\gspa RECORD.axx RECORD.obj -h -l -v10 >> asm.log
echo SPEECH >> asm.log
\tools\gspa SPEECH.axx SPEECH.obj -h -l -v10 >> asm.log
echo ADJUST >> asm.log
\tools\gspa ADJUST.axx ADJUST.obj -h -l -v10 >> asm.log
echo AUDIT >> asm.log
\tools\gspa AUDIT.axx AUDIT.obj -h -l -v10 >> asm.log
echo TEST >> asm.log
\tools\gspa TEST.axx TEST.obj -h -l -v10 >> asm.log
echo DIAG >> asm.log
\tools\gspa DIAG.axx DIAG.obj -h -l -v10 >> asm.log
echo MENU >> asm.log
\tools\gspa MENU.axx MENU.obj -h -l -v10 >> asm.log
echo HSTD >> asm.log
\tools\gspa HSTD.axx HSTD.obj -h -l -v10 >> asm.log
echo MAKEPLR >> asm.log
\tools\gspa MAKEPLR.axx MAKEPLR.obj -h -l -v10 >> asm.log
echo MAKEPLR2 >> asm.log
\tools\gspa MAKEPLR2.axx MAKEPLR2.obj -h -l -v10 >> asm.log
echo SCREEN >> asm.log
\tools\gspa SCREEN.axx SCREEN.obj -h -l -v10 >> asm.log
echo SELECT3 >> asm.log
\tools\gspa SELECT3.axx SELECT3.obj -h -l -v10 >> asm.log
echo SELECT4 >> asm.log
\tools\gspa SELECT4.axx SELECT4.obj -h -l -v10 >> asm.log
echo PLYRAT3 >> asm.log
\tools\gspa PLYRAT3.axx PLYRAT3.obj -h -l -v10 >> asm.log
echo PLYRDSQ2 >> asm.log
\tools\gspa PLYRDSQ2.axx PLYRDSQ2.obj -h -l -v10 >> asm.log
echo UNZIP >> asm.log
\tools\gspa UNZIP.axx UNZIP.obj -h -l -v10 >> asm.log
\tools\gsplnk bb.cmd > link.log
cd rom
\tools\vidram off
c:\tools\bigsrec <ff8.lrn > ..\srec.log
exit

