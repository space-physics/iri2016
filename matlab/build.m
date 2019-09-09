
cwd = fileparts(mfilename('fullpath'));

srcdir =   [cwd, filesep,'..'];
builddir = [cwd, filesep,'..',filesep,'build'];

assert(exist(srcdir,'dir')==7, ['source directory ',srcdir,' does not exist'])

try
  meson(srcdir, builddir)
catch
  cmake(srcdir, builddir)
end
