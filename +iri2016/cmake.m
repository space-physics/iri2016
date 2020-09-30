function cmake(srcdir)
% build project with CMake
arguments
  srcdir (1,1) string
end

cmd = "ctest -S" + fullfile(srcdir, "setup.cmake") +  " -VV";

ret = system(cmd);
assert(ret==0, 'failed to build IRI')

end
