function cmake(srcdir)
% build project with CMake
arguments
  srcdir (1,1) string
end

cmd = "cmake --version";
ret = system(cmd);
if ret ~= 0
  error('iri2016:cmake:runtime_error', 'CMake not found')
end

cmd = "ctest -S " + fullfile(srcdir, "setup.cmake") +  " -VV";
disp(cmd)

ret = system(cmd);
assert(ret==0, 'failed to build IRI')

end
