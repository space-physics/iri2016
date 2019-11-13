function cmake(srcdir, builddir)
% assumes CMake >= 3.13
narginchk(2,2)
validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

tail = [' -S ', srcdir, ' -B ', builddir];

if ispc
  ccmd = ['cmake -G "MinGW Makefiles" -DCMAKE_SH="CMAKE_SH-NOTFOUND" ', tail];
else
  ccmd = ['cmake ',tail];
end

runcmd(ccmd)

runcmd(['cmake --build ',builddir,' --parallel'])

end
