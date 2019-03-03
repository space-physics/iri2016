
cwd = fileparts(mfilename('fullpath'));

srcdir =   [cwd, filesep,'..',filesep,'src'];
builddir = [cwd, filesep,'..',filesep,'build'];

assert(exist(srcdir,'dir')==7, ['source directory ',srcdir,' does not exist'])
assert(exist(builddir,'dir')==7, ['build directory ',builddir,' does not exist'])

try
  setup_meson(srcdir, builddir)
catch
  setup_cmake(srcdir, builddir)
end
