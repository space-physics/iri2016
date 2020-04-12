function cmake(srcdir, builddir)
% build program using CMake and default generator
% to specify generator with CMake >= 3.15 set environment variable CMAKE_GENERATOR

narginchk(2,2)

runcmd(['cmake -S', srcdir, ' -B', builddir])

runcmd(['cmake --build ',builddir,' --parallel'])

end
