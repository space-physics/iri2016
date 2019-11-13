function meson(srcdir, builddir)
narginchk(2,2)
validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

cmd = ['meson setup ',builddir,' ',srcdir];
if is_file([builddir, '/build.ninja'])
  cmd = [cmd, ' --wipe'];
end

runcmd(cmd)

runcmd(['meson test -C' ,builddir])

end
