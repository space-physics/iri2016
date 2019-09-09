function meson(srcdir, builddir)

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})


runcmd(['meson setup ',builddir,' ',srcdir])

runcmd(['ninja -C ' ,builddir])

end
