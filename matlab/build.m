function build(build_sys, srcdir, builddir)

switch build_sys
  case 'meson', meson(srcdir, builddir)
  case 'cmake', cmake(srcdir, builddir)
  otherwise, error(['unknown build system ', build_sys])
end
end % function