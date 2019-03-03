function setup_cmake(srcdir, builddir)
%% setup using CMake+Fortran compiler

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

[status, ret] = system('cmake --version');
if status~=0, error(ret), end
disp(ret)

tail = [' -S ', srcdir, ' -B ', builddir];

if ispc
  ccmd = ['cmake -G "MinGW Makefiles" -DCMAKE_SH="CMAKE_SH-NOTFOUND" ', tail];
else
  ccmd = ['cmake ',tail];
end

[status, ret] = system(ccmd);
if status~=0, error(ret), end
disp(ret)

[status, ret] = system(['cmake --build ',builddir,' -j']);
if status~=0, error(ret), end
disp(ret)

disp('Fortran compilation complete')
end
