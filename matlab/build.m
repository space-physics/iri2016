function build(srcdir)
narginchk(1,1)

assert(is_folder(srcdir), 'source directory not found: %s', srcdir)

setup_file = fullfile(srcdir, '/setup.cmake');
assert(is_file(setup_file), 'could not find setup.cmake %', setup_file)

[ret, msg] = system(sprintf('ctest -S %s -VV', setup_file));
assert(ret==0, 'cmake failed to build %s', msg)

end
