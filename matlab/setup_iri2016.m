%% setup IRI2016 using Fortran compiler

if ispc
  ccmd = 'cmake -G "MinGW Makefiles" -DCMAKE_SH="CMAKE_SH-NOTFOUND" -S ../src -B ../build';
else
  ccmd = 'cmake -S ../src -B ../build';
end

[status, ret] = system(ccmd);
if status~=0, error(ret), end
disp(ret)

[status, ret] = system('cmake --build ../build -j');
if status~=0, error(ret), end
disp(ret)

disp('Fortran compilation complete')
