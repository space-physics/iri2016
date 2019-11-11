function cmake(srcdir, builddir)
narginchk(2,2)
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

runcmd(ccmd)

runcmd(['cmake --build ',builddir,' --parallel'])

end
