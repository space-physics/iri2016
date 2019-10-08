function meson(srcdir, builddir)

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

assert(is_folder(srcdir), ['source directory not found: ', srcdir])

exe = pyexe();

cmd = [exe, ' -m meson setup ',builddir,' ',srcdir]

runcmd(cmd)

runcmd([exe, ' -m meson test -C' ,builddir])

end
