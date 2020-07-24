function build(srcdir)
narginchk(1,1)

assert(is_folder(srcdir), 'source directory not found: %s', srcdir)

[ret, msg] = system('ctest -S ', srcdir, ' setup.cmake -VV');
assert(ret==0, 'cmake failed to build %s', msg)

end
