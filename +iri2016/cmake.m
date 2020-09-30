function cmake(srcdir)
% build project with CMake
arguments
  srcdir (1,1) string
end

fix_macos()

cmd = "cmake --version";
ret = system(cmd);
if ret ~= 0
  error('iri2016:cmake:runtime_error', 'CMake not found')
end

cmd = "ctest -S " + fullfile(srcdir, "setup.cmake") +  " -VV";
disp(cmd)

ret = system(cmd);
assert(ret==0, 'failed to build IRI')

end


function fix_macos()

%% MacOS PATH workaround
% Matlab does not seem to load .zshrc or otherwise pickup shell "export" like
% Matlab on Linux or Windows does, so we apply these MacOS-specific workaround
if ~ismac
  return
end

sys_path = getenv("PATH");
needed_paths = "/usr/local/bin";
for np = needed_paths
  if isfolder(np) && ~contains(sys_path, np)
    sys_path = np + pathsep + sys_path;
  end
end

setenv('PATH', sys_path)

end % function
