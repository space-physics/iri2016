function cmake(srcdir)
% build project with CMake
arguments
  srcdir char
end

ccmd = ['ctest -S ', fullfile(srcdir, 'setup.cmake'),  ' -VV'];

ret = system(ccmd);
assert(ret==0, 'failed to build IRI')

end
