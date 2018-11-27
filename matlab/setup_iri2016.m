%% setup IRI2016 using Fortran compiler

if ispc
  ccmd = ['cmake -G "MinGW Makefiles" -DCMAKE_SH="CMAKE_SH-NOTFOUND" ..\src'];
else
  ccmd = ['cmake ../src'];
end

cwd = fileparts(mfilename('fullpath'));
cd([cwd,filesep,'..',filesep,'bin'])

[status, ret] = system(ccmd);
if status~=0, error(ret), end
disp(ret)

[status, ret] = system('cmake --build .');
if status~=0, error(ret), end
disp(ret)

cd(cwd)

disp('Fortran compilation complete')
