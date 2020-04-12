function build(srcdir, builddir, build_sys)
narginchk(2,3)

assert(is_folder(srcdir), ['source directory not found: ', srcdir])

if nargin < 3
  if system('cmake --version') == 0
    build_sys = 'cmake';
  elseif system('meson --version') == 0 && system('ninja --version') == 0
    build_sys = 'meson';
  else
    error('could not find Meson + Ninja or CMake')
  end
end

switch build_sys
  case 'meson', meson(srcdir, builddir)
  case 'cmake', cmake(srcdir, builddir)
  otherwise, error(['unknown build system ', build_sys])
end
end % function
