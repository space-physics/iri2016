function meson(srcdir, builddir)
narginchk(2,2)
validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

assert(is_folder(srcdir), ['source directory not found: ', srcdir])

exe = pyexe();

cmd = [exe, ' -m meson setup ',builddir,' ',srcdir];
if is_file([builddir, '/build.ninja'])
  cmd = [cmd, ' --wipe'];
end

runcmd(cmd)

runcmd([exe, ' -m meson test -C' ,builddir])

end
